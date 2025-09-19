from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import folium
from folium.plugins import HeatMap

from patched.paths import WEB_OUTPUTS_DIR


def _build_heat_data(rows: Iterable[Sequence[float]]) -> list[list[float]]:
    return [list(item) for item in rows]


def create_heatmap(
    df,
    map_center,
    weight_threshold,
    *,
    zoom_start: int = 12,
    output_file: str | Path = 'heatmap.html',
):
    """Create and persist an interactive heatmap."""
    fmap = folium.Map(location=map_center, zoom_start=zoom_start, tiles='CartoDB positron')

    heat_rows = (
        [row['latitude'], row['longitude'], float(row['weight'])]
        for _, row in df.iterrows()
        if float(row['weight']) >= float(weight_threshold)
    )
    heat_data = _build_heat_data(heat_rows)

    for _, row in df.iterrows():
        if float(row['weight']) >= float(weight_threshold):
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['Band name:']} · {row['Band Instagram handle:']}",
            ).add_to(fmap)

    HeatMap(data=heat_data, radius=15).add_to(fmap)

    output_path = Path(output_file)
    if not output_path.is_absolute():
        output_path = WEB_OUTPUTS_DIR / output_path.name

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fmap.save(str(output_path))

    return output_path
