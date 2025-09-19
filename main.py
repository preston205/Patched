from __future__ import annotations

from pathlib import Path

from patched import (
    DATA_PROCESSED_DIR,
    DATA_RAW_DIR,
    WEB_OUTPUTS_DIR,
    create_heatmap,
    lat_long,
)


def main() -> None:
    artist_data = DATA_RAW_DIR / 'data.csv'
    locals_data = DATA_RAW_DIR / 'Locals.csv'
    genre_matrix = DATA_RAW_DIR / 'genre_matrix.csv'

    looking_for = input('What genre are you looking for? ')
    map_center = (40.758701, -111.876183)
    weight_threshold = int(input('What weight threshold would you like to apply? '))

    df = lat_long(
        artist_data,
        looking_for,
        locals_file=locals_data,
        genre_matrix_file=genre_matrix,
        output_path=DATA_PROCESSED_DIR / 'updated_data.csv',
    )

    output_path = create_heatmap(
        df,
        map_center,
        weight_threshold,
        output_file=WEB_OUTPUTS_DIR / 'heatmap.html',
    )

    print(f'Heatmap saved to {output_path}')


if __name__ == '__main__':
    main()
