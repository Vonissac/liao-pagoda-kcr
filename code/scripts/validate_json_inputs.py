from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from package_paths import DATA_DIR, ensure_output_dir
from utils import read_json_with_leading_comments, write_csv_rows


JSON_INPUT_FILES = [
    DATA_DIR / "kg" / "inputs" / "bm25_corpus_raw.json",
    DATA_DIR / "kg" / "inputs" / "kg_testset.json",
    DATA_DIR / "kg" / "raw_results" / "bm25_raw_results.json",
    DATA_DIR / "kg" / "raw_results" / "kg_raw_results.json",
    DATA_DIR / "cbr" / "inputs" / "cbr_weights.json",
    DATA_DIR / "cbr" / "inputs" / "spatial_node_info.json",
    DATA_DIR / "cbr" / "inputs" / "testset_ground_truth.json",
]


def leading_comments(path: Path) -> list[str]:
    comments: list[str] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.lstrip().startswith("#"):
            comments.append(line)
            continue
        if line.strip():
            break
    return comments


def is_valid_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return False
    return True


def describe_payload(payload: Any) -> tuple[str, int | str]:
    if isinstance(payload, list):
        return "list", len(payload)
    if isinstance(payload, dict):
        return "dict", len(payload)
    return type(payload).__name__, ""


def main() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in JSON_INPUT_FILES:
        comments = leading_comments(path)
        payload = read_json_with_leading_comments(path)
        payload_type, payload_count = describe_payload(payload)
        rows.append({
            "path": str(path.relative_to(DATA_DIR.parent)),
            "leading_comment_count": str(len(comments)),
            "payload_type": payload_type,
            "payload_count": str(payload_count),
            "json_loadable_without_comment_handling": str(is_valid_json(path)),
            "valid_for_reproduction": "True",
        })

    write_csv_rows(
        ensure_output_dir() / "json_input_validation.csv",
        rows,
        [
            "path",
            "leading_comment_count",
            "payload_type",
            "payload_count",
            "json_loadable_without_comment_handling",
            "valid_for_reproduction",
        ],
    )
    return rows


if __name__ == "__main__":
    main()
