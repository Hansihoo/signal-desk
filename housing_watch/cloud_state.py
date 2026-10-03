"""Durable GitHub Release snapshots for ephemeral collection runners."""

import argparse
import base64
import json
import os
import re
import sqlite3
import subprocess
import tarfile
import tempfile
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


TAG_PREFIX = "signal-desk-data-"
ASSET_PATTERN = r"state-[A-Za-z0-9_.-]+\.tar\.gz"


def gh(*args, input_text=None):
    result = subprocess.run(["gh"] + list(args), input=input_text, check=True, capture_output=True, text=True)
    return result.stdout


def releases(repo):
    pages = json.loads(gh("api", "--paginate", "--slurp", "repos/%s/releases?per_page=100" % repo))
    return [release for page in pages for release in page if re.fullmatch(TAG_PREFIX + r"\d{4}-\d{2}", release["tag_name"])]


def latest_asset(release_list):
    candidates = [(asset["created_at"], asset["id"], release["tag_name"], asset["name"])
                  for release in release_list for asset in release.get("assets", [])
                  if re.fullmatch(ASSET_PATTERN, asset["name"])]
    return max(candidates) if candidates else None


def create_archive(root, destination):
    root, destination = Path(root), Path(destination)
    database = root / "data/housing_watch.sqlite"
    if not database.is_file() or not (root / "site/archive/index.json").is_file():
        raise ValueError("A collected database and briefing archive are required for backup.")
    with closing(sqlite3.connect(str(database))) as source:
        tables = {row[0] for row in source.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "job_items" in tables and source.execute("SELECT COUNT(*) FROM job_items").fetchone()[0]:
            raise ValueError("Public cloud backup refuses databases containing local/private job imports.")
        with tempfile.TemporaryDirectory() as temp:
            backup_path = Path(temp) / "housing_watch.sqlite"
            with closing(sqlite3.connect(str(backup_path))) as backup:
                source.backup(backup)
            with tarfile.open(str(destination), "w:gz") as archive:
                archive.add(str(backup_path), arcname="data/housing_watch.sqlite")
                for directory in (root / "data/raw", root / "site"):
                    if not directory.exists():
                        continue
                    for path in sorted(directory.rglob("*")):
                        if path.is_symlink():
                            raise ValueError("Snapshot must not contain symbolic links.")
                        if path.is_file() and path.name != ".gitkeep":
                            archive.add(str(path), arcname=path.relative_to(root).as_posix())


def restore_archive(archive_path, root):
    root = Path(root).resolve()
    with tarfile.open(str(archive_path), "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            name = PurePosixPath(member.name)
            allowed = name == PurePosixPath("data/housing_watch.sqlite") or name.parts[:2] == ("data", "raw") or name.parts[:1] == ("site",)
            if not allowed or name.is_absolute() or ".." in name.parts or "\\" in member.name or not (member.isfile() or member.isdir()):
                raise ValueError("Unsafe snapshot member: %s" % member.name)
            target = root.joinpath(*name.parts).resolve()
            if root not in target.parents:
                raise ValueError("Snapshot path escapes the target directory.")
        # Validate every member before writing any data; never use extractall.
        for member in members:
            target = root.joinpath(*PurePosixPath(member.name).parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source, target.open("wb") as output:
                    while True:
                        chunk = source.read(1024 * 1024)
                        if not chunk:
                            break
                        output.write(chunk)
    with closing(sqlite3.connect(str(root / "data/housing_watch.sqlite"))) as conn:
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Restored SQLite database failed integrity validation.")


def record_monthly_operation(repo, root):
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    endpoint = "repos/%s/contents/docs/ai/CLOUD_STATUS.md" % repo
    existing = json.loads(gh("api", endpoint))
    text = base64.b64decode(existing["content"]).decode("utf-8")
    if "Month: " + month in text:
        return
    status = json.loads((Path(root) / "site/status.json").read_text(encoding="utf-8"))
    run_url = "https://github.com/%s/actions/runs/%s" % (repo, os.environ["GITHUB_RUN_ID"])
    content = "# Cloud collection status\n\nMonth: %s\n\n- Successful refresh and deployment: %s\n- Public records: %d\n- Run: %s\n\nThis monthly operational record keeps repository activity visible. Source data and generated pages remain outside Git commits.\n" % (month, status["generated_at"], status["count"], run_url)
    payload = {"message": "[운영] 월간 수집 상태 기록 [skip ci]\n\n- 공개 자료 수집과 사이트 배포 완료 기록\n- 자동 수집 실행 링크 갱신", "sha": existing["sha"], "content": base64.b64encode(content.encode("utf-8")).decode("ascii")}
    gh("api", endpoint, "--method", "PUT", "--input", "-", input_text=json.dumps(payload))
    print("Updated monthly operation record: %s" % month)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["restore", "save", "record"])
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    if not args.repo:
        parser.error("--repo or GITHUB_REPOSITORY is required")
    if args.command == "record":
        record_monthly_operation(args.repo, args.root)
        return
    release_list = releases(args.repo)
    with tempfile.TemporaryDirectory() as temp:
        if args.command == "restore":
            latest = latest_asset(release_list)
            if not latest:
                if release_list:
                    raise ValueError("Existing state releases have no restorable snapshot; refusing a fresh start.")
                print("No previous cloud snapshot. Starting the first collection.")
                return
            _, _, tag, name = latest
            gh("release", "download", tag, "--repo", args.repo, "--pattern", name, "--dir", temp)
            restore_archive(Path(temp) / name, args.root)
            print("Restored %s / %s" % (tag, name))
        else:
            now = datetime.now(timezone.utc)
            tag = TAG_PREFIX + now.strftime("%Y-%m")
            name = "state-%s-%s-%s.tar.gz" % (now.strftime("%Y%m%dT%H%M%SZ"), os.environ.get("GITHUB_RUN_ID", "manual"), os.environ.get("GITHUB_RUN_ATTEMPT", "1"))
            path = Path(temp) / name
            create_archive(args.root, path)
            if not any(release["tag_name"] == tag for release in release_list):
                gh("release", "create", tag, "--repo", args.repo, "--target", os.environ.get("GITHUB_SHA", "main"), "--prerelease", "--title", "Signal Desk data " + now.strftime("%Y-%m"), "--notes", "Public-source collection state and dated briefings. Each snapshot is retained for recovery; generated data is not committed to source history.")
            gh("release", "upload", tag, str(path), "--repo", args.repo)
            print("Saved %s / %s (%d bytes)" % (tag, name, path.stat().st_size))


if __name__ == "__main__":
    main()
