from __future__ import annotations

import hashlib
from pathlib import Path

from package_paths import DATA_DIR, PACKAGE_DIR, ensure_output_dir
from utils import write_csv_rows


SKIP_DIRS = {".git", ".venv", "__pycache__"}
SKIP_PREFIXES = {"reproducibility/output"}
SKIP_FILES = {"data/DATA_MANIFEST.csv", "docs/PACKAGE_SUMMARY.json", ".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest() -> list[dict]:
    rows = []
    for path in sorted(PACKAGE_DIR.rglob("*")):
        if path.is_dir() or any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(PACKAGE_DIR).as_posix()
        if (
            rel in SKIP_FILES
            or path.name == ".DS_Store"
            or path.suffix in SKIP_SUFFIXES
            or any(rel == prefix or rel.startswith(f"{prefix}/") for prefix in SKIP_PREFIXES)
        ):
            continue
        rows.append({
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    return rows


def build_data_manifest() -> list[dict]:
    rows = []
    for path in sorted(DATA_DIR.rglob("*")):
        if path.is_dir() or any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(PACKAGE_DIR).as_posix()
        if (
            rel == "data/DATA_MANIFEST.csv"
            or path.name == ".DS_Store"
            or path.suffix in SKIP_SUFFIXES
        ):
            continue
        rows.append({
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    write_csv_rows(DATA_DIR / "DATA_MANIFEST.csv", rows, ["path", "bytes", "sha256"])
    return rows


def main() -> list[dict]:
    rows = build_manifest()
    out = ensure_output_dir() / "package_manifest.csv"
    write_csv_rows(out, rows, ["path", "bytes", "sha256"])
    return rows


if __name__ == "__main__":
    main()
