from __future__ import annotations

import json
import sys

from build_manifest import build_data_manifest, main as build_manifest
from package_paths import DATA_DIR, ensure_output_dir
from project_kg_equivalence import main as project_kg_equivalence
from reproduce_metrics import main as reproduce_metrics
from validate_json_inputs import main as validate_json_inputs
from verify_package import main as verify_package
from utils import read_csv_rows


def count_rows(path):
    return len(read_csv_rows(path)) if path.is_file() else 0


def main() -> int:
    if sys.version_info < (3, 8):
        print("Python 3.8 or later is required for this reproducibility package.", file=sys.stderr)
        return 2
    out_dir = ensure_output_dir()
    json_validation = validate_json_inputs()
    data_manifest = build_data_manifest()
    project_kg_pagodas = count_rows(DATA_DIR / "kg" / "project_kg_execution_tables" / "pagodas.csv")
    kg_equivalence = project_kg_equivalence()
    verification = verify_package()
    metrics = reproduce_metrics()
    manifest = build_manifest()
    summary = {
        "verification": verification,
        "metrics": metrics,
        "project_kg_equivalence": {
            "kg_retrieval_pass": kg_equivalence["kg_retrieval"]["passes_reference_baseline"],
            "cbr_retrieval_pass": kg_equivalence["cbr_retrieval"]["passes_reference_baseline"],
        },
        "json_input_files_checked": len(json_validation),
        "all_json_inputs_valid_for_reproduction": all(
            row["valid_for_reproduction"] == "True" for row in json_validation
        ),
        "data_manifest_file_count": len(data_manifest),
        "project_kg_execution_tables": {
            "pagodas": project_kg_pagodas,
            "role": "released tabular query and CBR execution view; full LP-KG scale is reported under data/kg/full_lpkg_neo4j_export",
        },
        "manifest_file_count": len(manifest),
    }
    (out_dir / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if verification["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
