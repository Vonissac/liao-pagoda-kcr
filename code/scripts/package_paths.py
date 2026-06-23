from __future__ import annotations

from pathlib import Path


CODE_DIR = Path(__file__).resolve().parents[1]
PACKAGE_DIR = CODE_DIR.parent
DATA_DIR = PACKAGE_DIR / "data"
OUTPUT_DIR = PACKAGE_DIR / "reproducibility" / "output"


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR
