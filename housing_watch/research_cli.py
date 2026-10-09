"""CLI boundary for opt-in automatic research and deterministic release checks."""

import json
from pathlib import Path

from .research_workflow import canonical, digest, make_plan, run_research, verify_release


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def add_commands(sub):
    plan = sub.add_parser("research-plan", help="derive a question/evidence plan without network or model calls")
    plan.add_argument("--input", required=True)
    plan.add_argument("--output", required=True)
    check = sub.add_parser("research-check", help="check report-v1 against original/analysis/review quality packages")
    check.add_argument("--input", required=True)
    check.add_argument("--quality", required=True)
    audit = sub.add_parser("research-audit", help="show which configured editions have current quality packages; no network/model calls")
    audit.add_argument("--output", required=True)
    run = sub.add_parser("research-run", help="opt-in bounded collect/analyze/write/review workflow; does not publish")
    run.add_argument("--input", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--raw-root", required=True, help="existing registered raw-snapshot directory")
    run.add_argument("--model", required=True, help="explicit OpenAI model ID; OPENAI_API_KEY required")
    run.add_argument("--reviewer-model", help="optional separate reviewer model; same model in a fresh context by default")
    run.add_argument("--max-calls", type=int, default=10)
    run.add_argument("--max-fetches", type=int, default=6)
    run.add_argument("--max-rounds", type=int, default=2)
    run.add_argument("--max-output-tokens", type=int, default=10000)
    run.add_argument("--max-input-chars", type=int, default=120000)
    run.add_argument("--max-age-hours", type=float, default=24)
    run.add_argument("--discover", action="store_true", help="opt into at most one paid web-search tool call, restricted to request.allowed_domains")
    run.add_argument("--import-reviewed", action="store_true", help="store a ready report in SQLite revisions after quality checks; does not deploy")


def handle(args, conn=None):
    if args.command == "research-plan":
        plan = make_plan(read_json(args.input))
        Path(args.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Plan: %s; no network/model calls" % args.output)
        return 0
    if args.command == "research-check":
        from .research_data import load_report_input
        packages = read_json(args.quality)["packages"]
        verify_release(load_report_input(args.input), packages)
        print("Quality gate passed: %d reports (not human reader approval)" % len(packages))
        return 0
    if args.command == "research-audit":
        from .research_data import load_publication
        _, batches = load_publication()
        current = {}
        for batch_id, reports in batches:
            packages = {p["draft"]["report"]["id"]: p for p in (getattr(reports, "quality_packages", None) or [])}
            for report in reports:
                current[report["id"]] = {"id": report["id"], "title": report["title"], "batch": batch_id,
                    "status": "gated_agent_review" if report["id"] in packages else "needs_substantive_review",
                    "report_hash": digest(report)}
        Path(args.output).write_text(json.dumps({"scope": "configured editions; not human comprehension approval", "reports": list(current.values())}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Configured quality coverage: %d gated, %d need substantive review; no model calls" %
              (sum(r["status"] == "gated_agent_review" for r in current.values()), sum(r["status"] != "gated_agent_review" for r in current.values())))
        return 0
    from .research_provider import ResponsesProvider
    provider = ResponsesProvider(args.model, args.reviewer_model, discovery=args.discover)
    package = run_research(conn, read_json(args.input), provider, args.raw_root,
                           limits={"calls": args.max_calls, "fetches": args.max_fetches, "rounds": args.max_rounds,
                                   "output_tokens": args.max_output_tokens, "input_chars": args.max_input_chars,
                                   "max_age_hours": args.max_age_hours})
    Path(args.output).write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if package["status"] == "ready":
        reports = [package["draft"]["report"]]
        verify_release(reports, [package])
        destination = Path(args.output)
        report_path = destination.with_name(destination.stem + ".reports.json")
        quality_path = destination.with_name(destination.stem + ".quality.json")
        report_path.write_text(json.dumps({"schema_version": 1, "reports": reports}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        quality_path.write_text(json.dumps({"packages": [package]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Ready artifacts: %s; %s" % (report_path, quality_path))
        if args.import_reviewed:
            from .research_data import import_reports
            print("Reviewed import: %s" % import_reports(conn, reports))
    print("Research: %s; usage=%s; issues=%s" % (package["status"], canonical(package["usage"]), canonical(package["issues"])))
    return 0 if package["status"] == "ready" else 1
