from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = PACKAGE_DIR / "data" / "cbr" / "inputs" / "cbr_weights.json"


def load_cbr_config(path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def kg_time_step(era_text: Any, config: dict[str, Any] | None = None) -> float:
    """Era-step mapping preserved from the release CBR ranking logic."""
    text = str(era_text or "")
    default_steps = {
        "辽太": 1.0,
        "辽景": 1.8,
        "辽圣": 2.2,
        "辽兴": 2.6,
        "辽道": 3.0,
        "天祚": 3.5,
    }
    steps = (config or {}).get("era_step_map", default_steps)
    for key, value in steps.items():
        if key in text:
            return value
    return (config or {}).get("era_default_step", 2.5)


def same_story(target: dict[str, str], candidate: dict[str, str]) -> int:
    try:
        return int(float(target.get("层数", 0) or 0) == float(candidate.get("层数", 0) or 0))
    except ValueError:
        return 0


def same_dao(target: dict[str, str], candidate: dict[str, str]) -> int:
    dao = target.get("辽代五京/道", "")
    return int(bool(dao) and dao != "未知" and dao == candidate.get("辽代五京/道", ""))


def era_similarity(target: dict[str, str], candidate: dict[str, str], config: dict[str, Any]) -> float:
    delta = abs(kg_time_step(target.get("建造时期"), config) - kg_time_step(candidate.get("建造时期"), config))
    denominator = config.get("time_params", {}).get("era_step_denominator", 0.5)
    return math.exp(-(delta ** 2) / denominator)


def cbr_score(target: dict[str, str], candidate: dict[str, str], config: dict[str, Any]) -> dict[str, Any]:
    weights = config["weights"]
    geo_params = config["geo_params"]
    dao_match = same_dao(target, candidate)
    time_score = era_similarity(target, candidate, config)
    story_match = same_story(target, candidate)
    modern_province_match = int(target.get("现代省份") == candidate.get("现代省份"))
    total = (
        weights["geo_spatial"] * geo_params["dao"] * dao_match
        + weights["time_series"] * time_score
        + weights["physical_attr"] * story_match
        + weights["geo_spatial"] * geo_params["province"] * modern_province_match
    )
    return {
        "塔名": candidate["塔名"],
        "total_score": round(total, 4),
        "rank_factors": [
            round(total, 4),
            dao_match,
            time_score,
            story_match,
        ],
        "details": {
            "space_dao": dao_match,
            "era": time_score,
            "modality_story": story_match,
            "modern_province_tiebreak": modern_province_match,
        },
    }


def run_leave_one_out(pagodas: list[dict[str, str]]) -> dict[str, list[dict[str, Any]]]:
    config = load_cbr_config()
    results: dict[str, list[dict[str, Any]]] = {}
    for target in pagodas:
        candidates = [
            row for row in pagodas
            if row["塔名"] != target["塔名"] and row.get("塔类型") == target.get("塔类型")
        ]
        if not candidates:
            candidates = [row for row in pagodas if row["塔名"] != target["塔名"]]
        scored = [cbr_score(target, candidate, config) for candidate in candidates]
        results[target["塔名"]] = sorted(
            scored,
            key=lambda row: tuple(row["rank_factors"]),
            reverse=True,
        )
    return results
