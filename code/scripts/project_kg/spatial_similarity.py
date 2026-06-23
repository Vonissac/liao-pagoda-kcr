from __future__ import annotations

import math
import re
from typing import Mapping


def dms_to_decimal(value: str) -> float | None:
    """Convert Chinese DMS coordinate text such as 119°18′25.78″ to decimal degrees."""
    if not value:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)\D+(\d+(?:\.\d+)?)?\D*(\d+(?:\.\d+)?)?", value)
    if not match:
        return None
    degrees = float(match.group(1))
    minutes = float(match.group(2) or 0)
    seconds = float(match.group(3) or 0)
    return degrees + minutes / 60 + seconds / 3600


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Neo4j point.distance parity fallback using a standard spherical Haversine distance."""
    radius_km = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * radius_km * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def hierarchical_geo_score(
    target: Mapping[str, str],
    candidate: Mapping[str, str],
    params: Mapping[str, float],
) -> float:
    """Project KG equivalent of the CBR modern/historical geography score."""
    dao_score = params.get("dao", 0.0) if target.get("辽代五京/道") == candidate.get("辽代五京/道") else 0.0
    modern_score = 0.0
    if target.get("现代区县") and target.get("现代区县") == candidate.get("现代区县"):
        modern_score = params.get("county", 0.0)
    elif target.get("现代城市") and target.get("现代城市") == candidate.get("现代城市"):
        modern_score = params.get("city", 0.0)
    elif target.get("现代省份") and target.get("现代省份") == candidate.get("现代省份"):
        modern_score = params.get("province", 0.0)
    return max(dao_score, modern_score)

