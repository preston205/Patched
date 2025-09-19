from __future__ import annotations

import pandas as pd

from patched import DATA_RAW_DIR

def main() -> None:
    df = pd.read_csv(DATA_RAW_DIR / 'data.csv')
    print(df.head())


if __name__ == '__main__':
    main()
