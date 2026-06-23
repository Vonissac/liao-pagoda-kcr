from __future__ import annotations

from collections import defaultdict
from statistics import mean

from package_paths import DATA_DIR, ensure_output_dir
from project_kg_equivalence import evaluate_reference_kg_retrieval_equivalence, evaluate_project_kg_cbr_equivalence
from run_lpsl_stress_validator import main as run_lpsl_stress_validator
from utils import as_float, read_csv_rows, read_json, round4, write_json


def reproduce_kg() -> dict:
    raw_equivalence = evaluate_reference_kg_retrieval_equivalence()
    return {
        "source": "kg_testset.json + kg_raw_results.json",
        "query_record_count": raw_equivalence["query_record_count"],
        "unique_query_id_count": raw_equivalence["unique_query_id_count"],
        "overall_kg_p": raw_equivalence["macro_precision"],
        "overall_kg_r": raw_equivalence["macro_recall"],
        "overall_kg_f1": raw_equivalence["macro_f1"],
        "passes_reference_project_kg_baseline": raw_equivalence["passes_reference_baseline"],
        "note": "BM25 baseline remains recorded in kg_retrieval_summary.csv; project KG parity is checked against recorded LP-KG answer sets.",
    }


def reproduce_lpsl() -> dict:
    rows = read_csv_rows(DATA_DIR / "lpsl" / "lpsl_validation_inputs_results.csv")
    decisions = defaultdict(int)
    flags = defaultdict(int)
    for row in rows:
        decisions[row["Decision"]] += 1
        flags[row["Conflict_Flag"]] += 1
    replay = run_lpsl_stress_validator()
    return {
        "row_count": len(rows),
        "input_parameter_role": (
            "Randomized LPSL stress-test inputs; "
            "these values are not inference inputs and should not be interpreted "
            "as measured physical-ratio evidence."
        ),
        "decision_counts": dict(decisions),
        "conflict_flag_counts": dict(flags),
        "stress_validator_replay_pass": replay["pass"],
        "stress_validator_bounds": [replay["lower_bound"], replay["upper_bound"]],
    }


def reproduce_cbr() -> dict:
    data = evaluate_project_kg_cbr_equivalence()
    return {
        "source": "project_kg_execution_tables/pagodas.csv + testset_ground_truth.json",
        "valid_samples": data["valid_samples"],
        "hit_at_1": data["hit_at_1"],
        "hit_at_3": data["hit_at_3"],
        "hit_at_5": data["hit_at_5"],
        "mrr": data["mrr"],
        "passes_reference_project_kg_baseline": data["passes_reference_baseline"],
        "top5_order_matches_reference_cases": data["top5_order_matches_reference_cases"],
    }


def reproduce_cot() -> dict:
    rows = read_csv_rows(DATA_DIR / "cot_ablation" / "ablation_summary.csv")
    by_section = defaultdict(list)
    by_model_section = defaultdict(list)
    for row in rows:
        section = row["section"]
        model = row["model"]
        ned_mean = as_float(row["ned_mean"])
        by_section[section].append(ned_mean)
        by_model_section[f"{model}|{section}"].append(ned_mean)
    return {
        "section_summary": {
            section: {
                "cell_count": len(values),
                "mean_of_cell_means": round4(mean(values)),
                "min_cell_mean": round4(min(values)),
                "max_cell_mean": round4(max(values)),
            }
            for section, values in sorted(by_section.items())
        },
        "model_section_summary": {
            key: round4(mean(values))
            for key, values in sorted(by_model_section.items())
        },
    }


def main() -> dict:
    result = {
        "kg": reproduce_kg(),
        "lpsl": reproduce_lpsl(),
        "cbr": reproduce_cbr(),
        "cot_ablation": reproduce_cot(),
    }
    write_json(ensure_output_dir() / "reproduced_metrics.json", result)
    return result


if __name__ == "__main__":
    main()
