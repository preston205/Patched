from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def load_geodata(filepath: Path, required_cols: Iterable[str] | None = None) -> pd.DataFrame:
    """Load geographic data for heatmap visualisations."""
    data_path = Path(filepath)
    if not data_path.exists():
        raise FileNotFoundError(f"Geo data file not found: {data_path}")

    df = pd.read_csv(data_path)

    expected = list(required_cols or ('latitude', 'longitude', 'value'))
    if not all(col in df.columns for col in expected):
        raise ValueError(f'CSV must contain columns: {expected}')

    return df
