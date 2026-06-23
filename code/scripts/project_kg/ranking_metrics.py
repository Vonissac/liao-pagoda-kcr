from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PRF:
    precision: float
    recall: float
    f1: float


def precision_recall_f1(expected: Iterable[str], retrieved: Iterable[str]) -> PRF:
    expected_set = set(expected)
    retrieved_set = set(retrieved)
    if not expected_set and not retrieved_set:
        return PRF(1.0, 1.0, 1.0)
    precision = len(expected_set & retrieved_set) / len(retrieved_set) if retrieved_set else 0.0
    recall = len(expected_set & retrieved_set) / len(expected_set) if expected_set else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return PRF(precision, recall, f1)


def first_hit_rank(ranked_items: list[str], relevant_items: Iterable[str]) -> int | None:
    relevant = set(relevant_items)
    return next((idx + 1 for idx, name in enumerate(ranked_items) if name in relevant), None)


def hit_at_k(ranked_items: list[str], relevant_items: Iterable[str], k: int) -> int:
    relevant = set(relevant_items)
    return int(any(name in relevant for name in ranked_items[:k]))


def reciprocal_rank(ranked_items: list[str], relevant_items: Iterable[str]) -> float:
    rank = first_hit_rank(ranked_items, relevant_items)
    return 1 / rank if rank else 0.0

