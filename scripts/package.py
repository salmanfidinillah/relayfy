"""Package Relayfy source and assets with an optional WorkBuddy Skill entry."""

import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", ".browser-state", ".runtime"}
EXCLUDED_FILES = {"operator-keys.json", "manifest.json"}
LOCAL_CONFIG_PREFIXES = ("relayfy-connection", "reply", "mcp.local", "mcp.servers.local")


def include_file(path):
    relative = path.relative_to(ROOT)
    name = path.name.lower()
    if not path.is_file() or path.is_symlink() or EXCLUDED_DIRS.intersection(relative.parts):
        return False
    if name in EXCLUDED_FILES or name.startswith(LOCAL_CONFIG_PREFIXES):
        return False
    if name.startswith(".env") and name != ".env.example":
        return False
    if relative.parts[0] in {"web", "dist"} and name.startswith("."):
        return False
    return ".sqlite" not in name and path.suffix.lower() not in {".db", ".db-shm", ".db-wal", ".pyc", ".zip"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ROOT.parent / "deliverables/Relayfy_Web_Prototype.zip"))
    parser.add_argument("--workbuddy-skill", action="store_true", help="Place SKILL.md and the project at the ZIP root")
    args = parser.parse_args()
    output = Path(args.output)
    prefix = Path() if args.workbuddy_skill else Path("relayfy")
    paths = sorted(path for path in ROOT.rglob("*") if include_file(path))
    manifest = {
        "package": "Relayfy MVP - WorkBuddy runtime",
        "contains_runtime_secrets": False,
        "files": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in paths
        ],
    }
    manifest_text = json.dumps(manifest, indent=2) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as temp:
        archive_path = Path(temp) / "relayfy.zip"
        with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
            for path in paths:
                archive.write(path, (prefix / path.relative_to(ROOT)).as_posix())
            archive.writestr((prefix / "MANIFEST.json").as_posix(), manifest_text)
        with ZipFile(archive_path) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("ZIP integrity check failed")
            if args.workbuddy_skill and "SKILL.md" not in archive.namelist():
                raise RuntimeError("WorkBuddy ZIP must contain SKILL.md at the root")
        archive_path.replace(output)
    (ROOT / "MANIFEST.json").write_text(manifest_text, encoding="utf-8")
    print(json.dumps({
        "file": str(output),
        "files": len(paths) + 1,
        "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
