from __future__ import annotations

from collections import defaultdict
from typing import Any

from package_paths import DATA_DIR, ensure_output_dir
from utils import as_float, read_csv_rows, round4, write_csv_rows, write_json


LOWER_BOUND = -2.1
UPPER_BOUND = 3.0


def stress_decision(input_alpha: float) -> tuple[str, str]:
    if LOWER_BOUND <= input_alpha <= UPPER_BOUND:
        return "Accepted", "0"
    return "Rejected", "1"


def main() -> dict[str, Any]:
    rows = read_csv_rows(DATA_DIR / "lpsl" / "lpsl_validation_inputs_results.csv")
    out_rows: list[dict[str, Any]] = []
    mismatches = []
    decisions = defaultdict(int)
    flags = defaultdict(int)

    for idx, row in enumerate(rows, start=1):
        alpha = as_float(row["Input_Alpha"])
        decision, flag = stress_decision(alpha)
        decisions[decision] += 1
        flags[flag] += 1
        matches = decision == row["Decision"] and flag == row["Conflict_Flag"]
        if not matches:
            mismatches.append(idx)
        out_rows.append({
            "row_id": idx,
            "Input_Alpha": row["Input_Alpha"],
            "recorded_decision": row["Decision"],
            "recorded_conflict_flag": row["Conflict_Flag"],
            "recomputed_decision": decision,
            "recomputed_conflict_flag": flag,
            "matches_record": str(matches),
        })

    out_dir = ensure_output_dir()
    write_csv_rows(
        out_dir / "lpsl_stress_validator_recomputed.csv",
        out_rows,
        [
            "row_id",
            "Input_Alpha",
            "recorded_decision",
            "recorded_conflict_flag",
            "recomputed_decision",
            "recomputed_conflict_flag",
            "matches_record",
        ],
    )
    result = {
        "validator_role": "deterministic replay of recorded randomized interception/stress-test table",
        "input_parameter_role": (
            "Input_Alpha values are randomized stress-test inputs, not inference "
            "parameters and not measured physical-ratio evidence."
        ),
        "lower_bound": LOWER_BOUND,
        "upper_bound": UPPER_BOUND,
        "row_count": len(rows),
        "decision_counts": dict(decisions),
        "conflict_flag_counts": dict(flags),
        "mismatch_count": len(mismatches),
        "mismatch_row_ids": mismatches,
        "pass": len(mismatches) == 0,
        "accepted_fraction": round4(decisions["Accepted"] / len(rows)) if rows else 0,
    }
    write_json(out_dir / "lpsl_stress_validator_summary.json", result)
    return result


if __name__ == "__main__":
    main()
