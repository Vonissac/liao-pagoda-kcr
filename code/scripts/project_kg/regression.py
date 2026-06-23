from __future__ import annotations

from typing import Any, Iterable

from project_kg.ranking_metrics import first_hit_rank, hit_at_k, precision_recall_f1, reciprocal_rank
from utils import round4


def evaluate_answer_sets(testset: list[dict[str, Any]], answers_by_id: dict[str, list[str]], mode_by_id: dict[str, str] | None = None) -> dict[str, Any]:
    rows = []
    macro_p = []
    macro_r = []
    macro_f1 = []
    missing = []
    for item in testset:
        qid = item["qid"]
        retrieved = answers_by_id.get(qid)
        if retrieved is None:
            missing.append(qid)
            continue
        score = precision_recall_f1(item["expected_answer"], retrieved)
        macro_p.append(score.precision)
        macro_r.append(score.recall)
        macro_f1.append(score.f1)
        rows.append({
            "qid": qid,
            "category": item.get("category", ""),
            "mode": (mode_by_id or {}).get(qid, ""),
            "cypher_query": item.get("cypher_query", ""),
            "expected": item["expected_answer"],
            "retrieved": retrieved,
            "precision": round4(score.precision),
            "recall": round4(score.recall),
            "f1": round4(score.f1),
        })
    return {
        "query_record_count": len(rows),
        "unique_query_id_count": len({row["qid"] for row in rows}),
        "missing_result_ids": missing,
        "macro_precision": round4(sum(macro_p) / len(macro_p)) if macro_p else 0,
        "macro_recall": round4(sum(macro_r) / len(macro_r)) if macro_r else 0,
        "macro_f1": round4(sum(macro_f1) / len(macro_f1)) if macro_f1 else 0,
        "per_query": rows,
    }


def evaluate_rankings(rankings: dict[str, list[dict[str, Any]]], ground_truth: Iterable[dict[str, Any]]) -> dict[str, Any]:
    hit_counts = {1: 0, 3: 0, 5: 0}
    reciprocal_ranks = []
    per_case = []
    missing = []

    for item in ground_truth:
        pagoda_id = item["pagoda_id"]
        expected = set(item.get("gt_neighbors", []))
        ranked_rows = rankings.get(pagoda_id)
        if not ranked_rows or not expected:
            missing.append(pagoda_id)
            continue
        ranked_names = [row.get("塔名") for row in ranked_rows]
        first_hit = first_hit_rank(ranked_names, expected)
        rr = reciprocal_rank(ranked_names, expected)
        reciprocal_ranks.append(rr)
        for k in hit_counts:
            hit_counts[k] += hit_at_k(ranked_names, expected, k)
        per_case.append({
            "pagoda_id": pagoda_id,
            "expected_neighbors": sorted(expected),
            "top5": ranked_names[:5],
            "first_hit_rank": first_hit,
            "reciprocal_rank": round4(rr),
        })

    valid = len(per_case)
    hit_at = {f"hit_at_{k}": round4(v / valid) if valid else 0 for k, v in hit_counts.items()}
    mrr = round4(sum(reciprocal_ranks) / valid) if valid else 0
    return {
        "valid_samples": valid,
        "missing_or_unusable_cases": missing,
        **hit_at,
        "mrr": mrr,
        "per_case": per_case,
    }
