"""Versioned authoring choices. Frozen recipes are independent of report-v1.

Records describe the instructions selected for an edition, not reader approval.
No source collection, model invocation, rendering or publication occurs here.
"""

import hashlib
import json
import re
import sqlite3
from contextlib import closing
from pathlib import Path

from .timeutil import iso_utc

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "config/authoring/catalog.json"
VERSION = "authoring-recipe-1"
KINDS = {"policy", "profile", "method", "template"}
OVERRIDES = {"opening", "outline", "length", "tone", "visuals", "examples"}
REQUEST_FIELDS = ("id", "reader", "reader_question", "outcome", "research_type", "custom_profile", "authoring")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected nonempty authoring text")
    return value


def section_text(content, heading=None):
    """Select a Markdown section including its descendants, without rendering."""
    content = content.replace("\r\n", "\n")
    if heading is None:
        return content
    matches = list(re.finditer(r"^(#{1,6}) (.+)$", content, re.M))
    found = [i for i, m in enumerate(matches) if m[2] == heading]
    if len(found) != 1:
        raise ValueError("Source heading must exist exactly once: " + heading)
    index = found[0]
    start = matches[index]
    end = next((m.start() for m in matches[index + 1:] if len(m[1]) <= len(start[1])), len(content))
    return content[start.start():end]


def snapshot(source, root):
    name = text(source.get("path"))
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or Path(name).parts[0] not in {"docs", "skills"}:
        raise ValueError("Authoring instructions must stay in project docs/skills")
    content = section_text(path.read_text(encoding="utf-8"), source.get("section"))
    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if sha != source.get("sha256"):
        raise ValueError("Unreleased authoring change: " + name + "; review and release a new component version")
    return dict(source, text=content)


def check_artifact(artifact, root):
    """Fingerprint template implementations without sending code to the writer."""
    name = text(artifact.get("path"))
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or Path(name).parts[0] != "housing_watch":
        raise ValueError("Template artifacts must stay in housing_watch")
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if hashlib.sha256(content.encode("utf-8")).hexdigest() != artifact.get("sha256"):
        raise ValueError("Unreleased template implementation change: " + name)


def compose(request, catalog_path=None, root=None):
    """Resolve an explicit purpose plus document-local choices, then freeze text."""
    root = Path(root or ROOT)
    catalog = read_json(catalog_path or CATALOG)
    if catalog.get("schema_version") != 1:
        raise ValueError("Unsupported authoring catalog")
    options = request.get("authoring", {})
    if not isinstance(options, dict) or set(options) - {"profile", "template", "methods", "requirements", "preferences", "overrides"}:
        raise ValueError("Unsupported document authoring options")
    profile = options.get("profile", request.get("research_type"))
    defaults = catalog["defaults"].get(profile)
    if not defaults:
        raise ValueError("Choose an authoring profile by reader purpose before drafting")
    if request.get("research_type") not in (None, "custom", profile):
        raise ValueError("Authoring profile and research purpose disagree")
    brief = {k: text(request.get(k)) for k in ("id", "reader", "reader_question", "outcome")}
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", brief["id"]):
        raise ValueError("Invalid authoring document ID")
    brief["profile"] = profile
    methods = options.get("methods", defaults["methods"])
    if not isinstance(methods, list) or not methods or len(methods) != len(set(methods)):
        raise ValueError("Choose distinct authoring methods")
    selections = [("policy", catalog["policy"]), ("profile", defaults["profile"])]
    selections += [("method", m) for m in methods]
    selections += [("template", options.get("template", defaults["template"]))]
    entries = catalog["components"]
    if len({e["id"] for e in entries}) != len(entries):
        raise ValueError("Duplicate authoring catalog component")
    by_id = {e["id"]: e for e in entries}
    frozen = []
    for kind, key in selections:
        entry = by_id.get(key)
        if not entry or entry.get("kind") != kind or profile not in entry.get("supports", []):
            raise ValueError("Incompatible authoring component: " + str(key))
        if not re.fullmatch(r"\d+\.\d+\.\d+", entry.get("version", "")):
            raise ValueError("Component needs an explicit release version: " + key)
        for artifact in entry.get("artifacts", []):
            check_artifact(artifact, root)
        frozen.append(dict(entry, sources=[snapshot(s, root) for s in entry["sources"]]))
    overrides = options.get("overrides", [])
    if not isinstance(overrides, list):
        raise ValueError("Overrides must be document-local records")
    for change in overrides:
        if change.get("target") not in OVERRIDES or change.get("scope") != "document":
            raise ValueError("Only document-local presentation/content choices may override defaults")
        text(change.get("reason"))
        text(change.get("value"))
    if len({x["target"] for x in overrides}) != len(overrides):
        raise ValueError("Conflicting overrides for the same document choice")
    requirements = options.get("requirements", [])
    preferences = options.get("preferences", {})
    if not isinstance(requirements, list) or not all(isinstance(x, str) and x.strip() for x in requirements):
        raise ValueError("Requirements must be document-local text")
    if not isinstance(preferences, dict) or set(preferences) - OVERRIDES or not all(isinstance(x, str) and x.strip() for x in preferences.values()):
        raise ValueError("Unsupported document preferences")
    recipe = {"version": VERSION, "catalog_version": text(catalog.get("version")), "brief": brief,
              "request_hash": digest({k: request.get(k) for k in REQUEST_FIELDS}),
              "components": frozen, "requirements": requirements, "preferences": preferences,
              "overrides": overrides, "scope": "document", "status": "planned"}
    recipe["recipe_hash"] = digest(recipe)
    validate_recipe(recipe)
    return recipe


def for_request(request):
    frozen = request.get("authoring_recipe")
    if frozen is None:
        return compose(request)
    validate_recipe(frozen)
    if frozen["request_hash"] != digest({k: request.get(k) for k in REQUEST_FIELDS}):
        raise ValueError("Reader purpose/options changed; create a new authoring recipe")
    return frozen


def validate_recipe(recipe):
    if recipe.get("version") != VERSION or recipe.get("scope") != "document" or recipe.get("status") != "planned":
        raise ValueError("Unsupported frozen authoring recipe")
    if recipe.get("recipe_hash") != digest({k: v for k, v in recipe.items() if k != "recipe_hash"}):
        raise ValueError("Frozen authoring recipe was changed")
    profile = recipe["brief"]["profile"]
    components = recipe["components"]
    kinds = [c["kind"] for c in components]
    if any(kinds.count(k) != 1 for k in ("policy", "profile", "template")) or "method" not in kinds:
        raise ValueError("Incomplete authoring composition")
    if len({c["id"] for c in components}) != len(components):
        raise ValueError("Duplicate frozen authoring component")
    for component in components:
        if component["kind"] not in KINDS or profile not in component["supports"]:
            raise ValueError("Incompatible frozen component")
        for source in component["sources"]:
            if hashlib.sha256(source["text"].encode("utf-8")).hexdigest() != source["sha256"]:
                raise ValueError("Frozen instruction text differs from its source fingerprint")
    return recipe


def instructions(recipe, stage="write"):
    validate_recipe(recipe)
    selected = []
    for component in recipe["components"]:
        if stage in component.get("stages", []):
            selected += [s["text"] for s in component["sources"]]
    return {"recipe_hash": recipe["recipe_hash"], "brief": recipe["brief"],
            "requirements": recipe["requirements"], "preferences": recipe["preferences"],
            "overrides": recipe["overrides"], "guidance": selected,
            "precedence": "사실, 근거, 권한과 데이터 계약을 보존한다. 이번 명시 요청은 구성과 표현의 기본값을 구체화한다. 선택한 단계의 방법만 적용하고 과거 실행이나 승인을 만들지 않는다."}


def check_workspace(recipe, root=None):
    """A valid historical snapshot remains valid when current files change."""
    validate_recipe(recipe)
    root = Path(root or ROOT)
    changes = []
    for component in recipe["components"]:
        for source in component["sources"]:
            try:
                snapshot(source, root)
            except (OSError, ValueError) as exc:
                changes.append({"component": component["id"], "path": source["path"], "detail": str(exc)})
        for artifact in component.get("artifacts", []):
            try:
                check_artifact(artifact, root)
            except (OSError, ValueError) as exc:
                changes.append({"component": component["id"], "path": artifact["path"], "detail": str(exc)})
    return {"frozen_recipe_valid": True, "current_sources_changed": changes,
            "action": "Keep this recipe for its existing edition; compose a new recipe to adopt reviewed changes"}


def content_document(value, document_id, expected_kind=None):
    actual_kind = "report" if "reports" in value else "article" if "articles" in value else None
    if expected_kind and actual_kind and actual_kind != expected_kind:
        raise ValueError("Content container differs from the selected template")
    candidates = value.get("reports", value.get("articles", [value]))
    found = [x for x in candidates if x.get("id") == document_id]
    if len(found) != 1:
        raise ValueError("Content must contain exactly one matching document")
    return found[0]


def record(conn, recipe, content, edition):
    validate_recipe(recipe)
    if type(edition) is not int or edition < 1:
        raise ValueError("An explicit positive content edition is required")
    document_id = recipe["brief"]["id"]
    template = next(c for c in recipe["components"] if c["kind"] == "template")
    content = content_document(content, document_id, template.get("output_kind"))
    conn.execute("CREATE TABLE IF NOT EXISTS authoring_releases (id TEXT, version TEXT, digest TEXT NOT NULL, document TEXT NOT NULL, PRIMARY KEY(id,version))")
    conn.execute("CREATE TABLE IF NOT EXISTS authoring_records (document_id TEXT, edition INTEGER, content_hash TEXT NOT NULL, recipe_hash TEXT NOT NULL, document TEXT NOT NULL, created_at TEXT NOT NULL, PRIMARY KEY(document_id,edition))")
    conn.commit()
    entry = {"version": VERSION, "document_id": document_id, "edition": edition,
             "content_hash": digest(content), "recipe": recipe,
             "status": "author_declared_application", "meaning": "Instructions recorded; not a content/reader review or publication receipt"}
    with conn:
        previous = conn.execute("SELECT document FROM authoring_records WHERE document_id=? AND edition=?", (document_id, edition)).fetchone()
        if previous:
            if json.loads(previous[0]) != entry:
                raise ValueError("This edition already has different content/instructions; create a new edition")
            return {"changed": False, "record": entry}
        for component in recipe["components"]:
            sha = digest(component)
            old = conn.execute("SELECT digest FROM authoring_releases WHERE id=? AND version=?", (component["id"], component["version"])).fetchone()
            if old and old[0] != sha:
                raise ValueError("Component content changed without a version bump: " + component["id"])
            conn.execute("INSERT OR IGNORE INTO authoring_releases VALUES (?,?,?,?)", (component["id"], component["version"], sha, canonical(component)))
        conn.execute("INSERT INTO authoring_records VALUES (?,?,?,?,?,?)", (document_id, edition, entry["content_hash"], recipe["recipe_hash"], canonical(entry), iso_utc()))
    return {"changed": True, "record": entry}


def add_commands(sub):
    parser = sub.add_parser("authoring", help="compose, freeze and record document-specific writing instructions; offline")
    actions = parser.add_subparsers(dest="authoring_action", required=True)
    plan = actions.add_parser("plan")
    plan.add_argument("--input", required=True)
    plan.add_argument("--output", required=True)
    plan.add_argument("--catalog", default=str(CATALOG))
    check = actions.add_parser("check")
    check.add_argument("--recipe", required=True)
    bind = actions.add_parser("record")
    bind.add_argument("--recipe", required=True)
    bind.add_argument("--content", required=True)
    bind.add_argument("--edition", type=int, required=True)
    bind.add_argument("--db", default="data/authoring.sqlite")
    show = actions.add_parser("show")
    show.add_argument("--document", required=True)
    show.add_argument("--edition", type=int)
    show.add_argument("--db", default="data/authoring.sqlite")
    show.add_argument("--full", action="store_true", help="include the frozen instruction text")


def handle(args):
    if args.authoring_action == "plan":
        recipe = compose(read_json(args.input), args.catalog)
        with Path(args.output).open("x", encoding="utf-8", newline="\n") as file:
            file.write(json.dumps(recipe, ensure_ascii=False, indent=2) + "\n")
        result = {"output": args.output, "recipe_hash": recipe["recipe_hash"], "status": "planned"}
    elif args.authoring_action == "check":
        result = check_workspace(read_json(args.recipe))
    elif args.authoring_action == "record":
        recipe = read_json(args.recipe)
        content = read_json(args.content)
        validate_recipe(recipe)
        content_document(content, recipe["brief"]["id"])
        with closing(sqlite3.connect(args.db)) as conn:
            result = record(conn, recipe, content, args.edition)
        item = result["record"]
        result = dict(changed=result["changed"], document_id=item["document_id"], edition=item["edition"],
                      content_hash=item["content_hash"], recipe_hash=recipe["recipe_hash"], status=item["status"])
    else:
        path = Path(args.db).resolve()
        result = {"document_id": args.document, "status": "unrecorded", "records": []}
        if path.exists():
            with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as conn:
                if conn.execute("SELECT 1 FROM sqlite_master WHERE name='authoring_records'").fetchone():
                    rows = conn.execute("SELECT document FROM authoring_records WHERE document_id=? AND (? IS NULL OR edition=?) ORDER BY edition", (args.document, args.edition, args.edition)).fetchall()
                    result.update(status="recorded" if rows else "unrecorded", records=[json.loads(row[0]) for row in rows])
        if not args.full:
            for item in result["records"]:
                recipe = item.pop("recipe")
                item.update(recipe_hash=recipe["recipe_hash"], brief=recipe["brief"],
                            components=[{k: c[k] for k in ("id", "kind", "version")} for c in recipe["components"]],
                            requirements=recipe["requirements"], preferences=recipe["preferences"], overrides=recipe["overrides"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
