from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_json_with_leading_comments(path: Path) -> Any:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    while lines and lines[0].lstrip().startswith("#"):
        lines.pop(0)
    return json.loads("\n".join(lines))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def as_float(value: Any) -> float:
    if value is None or value == "":
        return float("nan")
    return float(value)


def round4(value: float) -> float:
    return round(float(value), 4)
