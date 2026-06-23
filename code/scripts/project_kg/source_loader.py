from __future__ import annotations

from pathlib import Path

from utils import read_csv_rows


def load_pagodas(execution_table_dir: Path) -> list[dict[str, str]]:
    return read_csv_rows(execution_table_dir / "pagodas.csv")
