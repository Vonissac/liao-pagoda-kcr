from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from package_paths import PACKAGE_DIR, ensure_output_dir
from utils import read_csv_rows, write_json


REQUIRED_FILES = [
    "README.md",
    "docs/DATA_AVAILABILITY.md",
    "docs/CODE_AVAILABILITY.md",
    "docs/RELEASE_BOUNDARY.md",
    "data/DATA_MANIFEST.csv",
    "data/kg/kg_retrieval_summary.csv",
    "data/kg/kg_retrieval_examples.csv",
    "data/kg/inputs/bm25_corpus_raw.json",
    "data/kg/inputs/kg_testset.json",
    "data/kg/raw_results/bm25_raw_results.json",
    "data/kg/raw_results/kg_raw_results.json",
    "data/kg/kg_source_registry.csv",
    "data/kg/full_lpkg_neo4j_export/nodes.csv",
    "data/kg/full_lpkg_neo4j_export/edges.csv",
    "data/kg/full_lpkg_neo4j_export/kg_full_summary.json",
    "data/kg/project_kg_execution_tables/pagodas.csv",
    "data/kg/project_kg_execution_tables/source_summary.json",
    "data/kg/project_kg_execution_tables/README.md",
    "data/lpsl/lpsl_validation_inputs_results.csv",
    "data/lpsl/lpsl_encodings.txt",
    "data/lpsl/measurement_source/liao_pagoda_basic_data.xlsx",
    "data/lpsl/measurement_source/liao_pagoda_vertical_measurements.xlsx",
    "data/cbr/cbr_loo_summary.json",
    "data/cbr/cbr_raw_rankings.json",
    "data/cbr/pagoda_attribute_corpus.csv",
    "data/cbr/inputs/cbr_weights.json",
    "data/cbr/inputs/spatial_node_info.json",
    "data/cbr/inputs/testset_ground_truth.json",
    "data/cot_ablation/ablation_summary.csv",
    "data/cot_ablation/raw_outputs/MANIFEST.csv",
    "data/cot_ablation/metrics/deepseek_ablation_summary.xlsx",
    "data/cot_ablation/metrics/glm_ablation_summary.xlsx",
    "data/cot_ablation/metrics/qwen_ablation_summary.xlsx",
    "data/cot_ablation/metrics/by_section/section_A_DeepSeek_V3_2_01_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_A_GLM_5_1_01_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_A_Qwen3_5_397B_A17B_02_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_B_DeepSeek_V3_2_02_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_B_GLM_5_1_01_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_B_Qwen3_5_397B_A17B_01_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_C_DeepSeek_V3_2_02_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_C_GLM_5_1_01_metrics.xlsx",
    "data/cot_ablation/metrics/by_section/section_C_Qwen3_5_397B_A17B_01_metrics.xlsx",
    "data/cot_ablation/sources/haotian/source_text.txt",
    "data/cot_ablation/sources/chaoyang_south/source_text.txt",
    "data/cot_ablation/sources/baitayu/source_text.txt",
    "data/supplementary_tables/s6_validation.csv",
    "data/cot_ablation/inputs/section_A_input_instruction.txt",
    "data/cot_ablation/inputs/section_B_input_instruction.txt",
    "data/cot_ablation/inputs/section_C_input_instruction.txt",
    "code/requirements.txt",
    "code/environment.yml",
    "code/scripts/validate_json_inputs.py",
]

REQUIRED_DIRS = [
    "code/scripts",
    "data",
    "data/cot_ablation/raw_outputs",
    "data/cot_ablation/metrics",
    "data/cot_ablation/metrics/by_section",
    "data/kg/project_kg_execution_tables",
    "docs",
]

IGNORED_RUNTIME_NAMES = {".DS_Store", "__MACOSX", ".ipynb_checkpoints"}
IGNORED_RUNTIME_SUFFIXES = {".pyc", ".pyo"}
EXPECTED_COT_MODELS = {"DeepSeek-V3.2", "GLM-5.1", "Qwen3.5-397B-A17B"}


def read_csv_count(path: Path) -> int:
    if not path.is_file():
        return 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def read_json_file(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def list_unexpected_runtime_files() -> list[str]:
    hits = []
    for path in sorted(PACKAGE_DIR.rglob("*")):
        rel = path.relative_to(PACKAGE_DIR).as_posix()
        if rel == "code/.venv" or rel.startswith("code/.venv/"):
            continue
        if ".git" in path.parts:
            continue
        if (
            path.name in IGNORED_RUNTIME_NAMES
            or path.suffix in IGNORED_RUNTIME_SUFFIXES
            or "__pycache__" in path.parts
            or ".venv" in path.parts
        ):
            hits.append(rel)
    return hits


def verify_data_manifest() -> dict:
    manifest_path = PACKAGE_DIR / "data" / "DATA_MANIFEST.csv"
    rows = []
    if manifest_path.is_file():
        with manifest_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    actual_paths = sorted(
        path.relative_to(PACKAGE_DIR).as_posix()
        for path in (PACKAGE_DIR / "data").rglob("*")
        if path.is_file()
        and path.relative_to(PACKAGE_DIR).as_posix() != "data/DATA_MANIFEST.csv"
        and path.name not in IGNORED_RUNTIME_NAMES
        and path.suffix not in IGNORED_RUNTIME_SUFFIXES
    )
    listed_paths = sorted(row.get("path", "") for row in rows)
    digest_mismatches = []
    for row in rows:
        rel = row.get("path", "")
        target = PACKAGE_DIR / rel
        if target.is_file() and row.get("sha256") != sha256(target):
            digest_mismatches.append(rel)
    return {
        "manifest_rows": len(rows),
        "actual_data_files": len(actual_paths),
        "path_match": listed_paths == actual_paths,
        "missing_from_manifest": sorted(set(actual_paths) - set(listed_paths)),
        "extra_in_manifest": sorted(set(listed_paths) - set(actual_paths)),
        "digest_mismatches": digest_mismatches,
    }


def verify_cbr_configuration() -> dict:
    config = read_json_file(PACKAGE_DIR / "data" / "cbr" / "inputs" / "cbr_weights.json")
    weights = config.get("weights", {})
    geo = config.get("geo_params", {})
    expected = {
        "geo_spatial": 0.4,
        "time_series": 0.4,
        "physical_attr": 0.2,
        "dao": 1.0,
        "province": 0.125,
        "sigma": 20.5,
        "threshold": 8,
        "shape_weight": 1.0,
        "story_penalty_beta": 0.0,
    }
    code_text = (PACKAGE_DIR / "code" / "scripts" / "project_kg" / "cbr_retrieval.py").read_text(encoding="utf-8")
    time_params = config.get("time_params", {})
    physical_params = config.get("physical_params", {})
    observed = {
        "geo_spatial": weights.get("geo_spatial"),
        "time_series": weights.get("time_series"),
        "physical_attr": weights.get("physical_attr"),
        "dao": geo.get("dao"),
        "province": geo.get("province"),
        "sigma": time_params.get("sigma"),
        "threshold": time_params.get("threshold"),
        "shape_weight": physical_params.get("shape_weight"),
        "story_penalty_beta": physical_params.get("story_penalty_beta"),
    }
    return {
        "expected": expected,
        "observed": observed,
        "matches_expected": observed == expected,
        "runtime_config_loader_present": "load_cbr_config" in code_text and "DEFAULT_CONFIG_PATH" in code_text,
        "configuration_notes_present": "S_CBR" in config.get("source_note", "") and "S_direct" in config.get("source_note", ""),
    }


def verify_requirements() -> dict:
    text = (PACKAGE_DIR / "code" / "requirements.txt").read_text(encoding="utf-8")
    entries = [
        line.strip() for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    return {
        "non_comment_dependency_count": len(entries),
        "standard_library_only_marker_present": "standard library" in text.lower(),
    }


def verify_raw_model_output_manifest() -> dict:
    base = PACKAGE_DIR / "data" / "cot_ablation" / "raw_outputs"
    manifest = base / "MANIFEST.csv"
    rows = []
    if manifest.is_file():
        with manifest.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    listed = []
    for row in rows:
        rel = row.get("relative_path", "") or row.get("path", "")
        if rel.startswith("data/cot_ablation/raw_outputs/"):
            rel = rel.removeprefix("data/cot_ablation/raw_outputs/")
        if rel.startswith("cot_ablation/raw_outputs/"):
            rel = rel.removeprefix("cot_ablation/raw_outputs/")
        listed.append(rel)
    listed = sorted(listed)
    actual = sorted(
        path.relative_to(base).as_posix()
        for path in base.rglob("*")
        if path.is_file()
        and path.name != "MANIFEST.csv"
        and path.name not in IGNORED_RUNTIME_NAMES
        and path.suffix not in IGNORED_RUNTIME_SUFFIXES
    )
    non_txt_raw_outputs = [rel for rel in actual if Path(rel).suffix.lower() != ".txt"]
    non_contiguous_sequences = []
    for directory in sorted({Path(rel).parent.as_posix() for rel in actual}):
        names = sorted(Path(rel).name for rel in actual if Path(rel).parent.as_posix() == directory)
        expected = [f"sample_{idx:03d}.txt" for idx in range(1, len(names) + 1)]
        if names != expected:
            non_contiguous_sequences.append({
                "directory": directory,
                "observed": names,
                "expected": expected,
            })
    return {
        "manifest_rows": len(rows),
        "actual_output_files": len(actual),
        "path_match": listed == actual,
        "only_txt_raw_outputs": not non_txt_raw_outputs,
        "non_txt_raw_outputs": non_txt_raw_outputs,
        "contiguous_sample_numbering": not non_contiguous_sequences,
        "non_contiguous_sequences": non_contiguous_sequences,
        "missing_from_manifest": sorted(set(actual) - set(listed)),
        "extra_in_manifest": sorted(set(listed) - set(actual)),
    }


def verify_cot_summary_sources() -> dict:
    summary_path = PACKAGE_DIR / "data" / "cot_ablation" / "ablation_summary.csv"
    rows = []
    if summary_path.is_file():
        with summary_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    source_paths = sorted({row.get("source_files", "") for row in rows if row.get("source_files", "")})
    missing_sources = [rel for rel in source_paths if not (PACKAGE_DIR / rel).is_file()]
    source_path_issues = [
        rel for rel in source_paths
        if "metrics" not in rel or not rel.endswith(".xlsx")
    ]
    return {
        "summary_rows": len(rows),
        "unique_source_files": len(source_paths),
        "missing_sources": missing_sources,
        "source_path_issues": source_path_issues,
        "uses_metrics": bool(source_paths) and all("metrics" in rel for rel in source_paths),
    }


def verify_kg_source_registry() -> dict:
    path = PACKAGE_DIR / "data" / "kg" / "kg_source_registry.csv"
    rows = []
    if path.is_file():
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    layers = {row.get("source_layer", "") for row in rows}
    statuses = {row.get("release_status", "") for row in rows}
    return {
        "row_count": len(rows),
        "has_full_lpkg_export": "Full LP-KG normalized export" in layers,
        "has_project_execution_tables": "Public project-KG execution tables" in layers,
        "documents_non_redistributed_source_carriers": "Restricted source carriers" in layers,
        "contains_not_redistributed_status": "not_redistributed" in statuses,
    }


def verify_cot_model_labels() -> dict:
    rows = read_csv_rows(PACKAGE_DIR / "data" / "cot_ablation" / "ablation_summary.csv")
    observed = sorted({row.get("model", "") for row in rows if row.get("model", "")})
    return {
        "observed_model_labels": observed,
        "expected_model_labels": sorted(EXPECTED_COT_MODELS),
        "unexpected_model_labels": sorted(set(observed) - EXPECTED_COT_MODELS),
    }


def verify() -> dict:
    missing_files = [path for path in REQUIRED_FILES if not (PACKAGE_DIR / path).is_file()]
    missing_dirs = [path for path in REQUIRED_DIRS if not (PACKAGE_DIR / path).is_dir()]
    raw_model_output_files = [
        path for path in (PACKAGE_DIR / "data" / "cot_ablation" / "raw_outputs").rglob("*.txt")
        if path.is_file()
    ]
    full_nodes = read_csv_count(PACKAGE_DIR / "data" / "kg" / "full_lpkg_neo4j_export" / "nodes.csv")
    full_edges = read_csv_count(PACKAGE_DIR / "data" / "kg" / "full_lpkg_neo4j_export" / "edges.csv")
    project_pagodas = read_csv_count(PACKAGE_DIR / "data" / "kg" / "project_kg_execution_tables" / "pagodas.csv")
    kg_summary = read_json_file(PACKAGE_DIR / "data" / "kg" / "full_lpkg_neo4j_export" / "kg_full_summary.json")
    unexpected_runtime_files = list_unexpected_runtime_files()
    data_manifest = verify_data_manifest()
    cbr_config = verify_cbr_configuration()
    requirements = verify_requirements()
    raw_model_output_manifest = verify_raw_model_output_manifest()
    cot_summary_sources = verify_cot_summary_sources()
    kg_source_registry = verify_kg_source_registry()
    cot_model_labels = verify_cot_model_labels()
    reproducibility_pass = (
        not unexpected_runtime_files
        and full_nodes == 3739
        and full_edges == 389891
        and project_pagodas == 68
        and len(raw_model_output_files) == 99
        and data_manifest["path_match"]
        and not data_manifest["digest_mismatches"]
        and cbr_config["matches_expected"]
        and cbr_config["runtime_config_loader_present"]
        and cbr_config["configuration_notes_present"]
        and requirements["standard_library_only_marker_present"]
        and raw_model_output_manifest["path_match"]
        and raw_model_output_manifest["only_txt_raw_outputs"]
        and raw_model_output_manifest["contiguous_sample_numbering"]
        and not cot_summary_sources["missing_sources"]
        and not cot_summary_sources["source_path_issues"]
        and cot_summary_sources["uses_metrics"]
        and not cot_model_labels["unexpected_model_labels"]
        and kg_source_registry["has_full_lpkg_export"]
        and kg_source_registry["has_project_execution_tables"]
        and kg_source_registry["documents_non_redistributed_source_carriers"]
        and kg_source_registry["contains_not_redistributed_status"]
    )
    return {
        "status": "pass" if not missing_files and not missing_dirs and reproducibility_pass else "fail",
        "missing_files": missing_files,
        "missing_dirs": missing_dirs,
        "checks": {
            "unexpected_runtime_files": unexpected_runtime_files,
            "data_manifest": data_manifest,
            "cbr_configuration": cbr_config,
            "requirements": requirements,
            "raw_model_output_manifest": raw_model_output_manifest,
            "cot_summary_sources": cot_summary_sources,
            "cot_model_labels": cot_model_labels,
            "kg_source_registry": kg_source_registry,
        },
        "full_lpkg_node_rows": full_nodes,
        "full_lpkg_relationship_rows": full_edges,
        "full_lpkg_summary": kg_summary.get("observed_counts", kg_summary),
        "project_kg_pagoda_rows": project_pagodas,
        "cot_raw_model_output_file_count": len(raw_model_output_files),
        "data_manifest_rows": read_csv_count(PACKAGE_DIR / "data" / "DATA_MANIFEST.csv"),
    }


def main() -> dict:
    result = verify()
    write_json(ensure_output_dir() / "package_verification.json", result)
    return result


if __name__ == "__main__":
    main()
