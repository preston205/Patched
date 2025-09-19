from __future__ import annotations

import random
from pathlib import Path
from typing import Optional

import pandas as pd

from patched.paths import DATA_PROCESSED_DIR


def lat_long(
    artist_file: Path,
    search_for: str,
    *,
    locals_file: Path,
    genre_matrix_file: Path,
    output_path: Optional[Path] = None,
) -> pd.DataFrame:
    """Augment artist data with coordinates and booking weights."""
    artist_path = Path(artist_file)
    locals_path = Path(locals_file)
    genre_matrix_path = Path(genre_matrix_file)

    if not artist_path.exists():
        raise FileNotFoundError(f"Artist data file not found: {artist_path}")
    if not locals_path.exists():
        raise FileNotFoundError(f"Locals lookup file not found: {locals_path}")
    if not genre_matrix_path.exists():
        raise FileNotFoundError(f"Genre matrix file not found: {genre_matrix_path}")

    df = pd.read_csv(artist_path)
    locals_df = pd.read_csv(locals_path)
    genre_matrix = pd.read_csv(genre_matrix_path)

    df['latitude'] = None
    df['longitude'] = None
    df['weight'] = None
    df['pull'] = None

    selected = genre_matrix[genre_matrix['Genre'] == search_for]
    if selected.empty:
        raise ValueError(f"Genre '{search_for}' not found in genre matrix")

    selected_row = selected.iloc[0]

    for idx, row in df.iterrows():
        insta_followers = df.at[idx, 'Instagram Follower count:']
        spotify_listeners = df.at[idx, 'Spotify monthly listeners']

        if insta_followers < spotify_listeners:
            pull = spotify_listeners
        else:
            pull_modifier = insta_followers / 3
            pull = min(insta_followers, spotify_listeners + pull_modifier)

        df.at[idx, 'pull'] = pull

        primary = row['Primary Genre']
        weight_primary = selected_row.get(primary, 0)
        weight_secondary = selected_row.get(row.get('Secondary Genre'), 0)
        weight_tertiary = selected_row.get(row.get('Tertiary Genre'), 0)

        weight_total = (10 * weight_primary) + (6 * weight_secondary) + (2 * weight_tertiary)
        df.at[idx, 'weight'] = weight_total

        match = locals_df[locals_df['City'] == row['location']]
        if not match.empty:
            base_lat = match.iloc[0]['latitude']
            base_long = match.iloc[0]['longitude']
            df.at[idx, 'latitude'] = base_lat + (random.randint(-10, 10) * 0.001)
            df.at[idx, 'longitude'] = base_long + (random.randint(-10, 10) * 0.001)
        else:
            print(f"No match found for location: {row['location']}")

    target_path = output_path or (DATA_PROCESSED_DIR / 'updated_data.csv')
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_path, index=False)

    required_cols = ['latitude', 'longitude']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f'CSV must contain columns: {required_cols}')

    return df
