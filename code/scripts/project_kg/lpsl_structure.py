from __future__ import annotations

import re
from difflib import SequenceMatcher


TOKEN_RE = re.compile(r"[A-Za-z]+(?:\[[^\]]+\])?|[a-z]\d+|\d+(?:\.\d+)?|[()+/@%<>,=-]")


def tokenize_lpsl(code: str) -> list[str]:
    return TOKEN_RE.findall(code or "")


def lpsl_sequence_similarity(a: str, b: str) -> float:
    """Token-sequence similarity used only as a transparent structural comparator."""
    return SequenceMatcher(None, tokenize_lpsl(a), tokenize_lpsl(b)).ratio()

