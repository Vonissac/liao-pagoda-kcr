from __future__ import annotations

import math
from typing import Any, Mapping


ERA_STEPS = {
    "辽太祖": 1, "神册": 1, "天赞": 1, "天显": 1,
    "辽太宗": 2, "会同": 2, "大同": 2,
    "辽世宗": 3, "天禄": 3,
    "辽穆宗": 4, "应历": 4,
    "辽景宗": 5, "保宁": 5, "乾亨": 5,
    "辽圣宗": 6, "统和": 6, "开泰": 6, "太平": 6,
    "辽兴宗": 7, "景福": 7, "重熙": 7,
    "辽道宗": 8, "清宁": 8, "咸雍": 8, "太康": 8, "大安": 8, "寿昌": 8,
    "辽天祚帝": 9, "乾统": 9, "天庆": 9, "保大": 9,
    "辽代早期": 3, "辽代中期": 6, "辽代晚期": 8,
}


def era_step(value: Any, default: int = 6, steps: Mapping[str, int] = ERA_STEPS) -> int:
    if isinstance(value, list):
        value = value[0] if value else ""
    text = str(value or "")
    for key, step in steps.items():
        if key in text:
            return step
    return default


def gaussian_era_similarity(a: Any, b: Any, sigma: float = 0.7) -> float:
    delta = abs(era_step(a) - era_step(b))
    return math.exp(-(delta ** 2) / (2 * sigma ** 2))


def cauchy_year_similarity(y1: Any, y2: Any, sigma: float = 12, threshold: float = 8) -> float:
    try:
        delta = abs(float(y1) - float(y2))
    except (TypeError, ValueError):
        return 0.0
    if delta <= threshold:
        return 1.0
    return 1 / (1 + (delta / sigma) ** 2)

