# Patched

Sandbox project

## Project layout

```
├── data
│   ├── processed
│   │   └── updated_data.csv
│   └── raw
│       ├── Locals.csv
│       ├── data.csv
│       └── genre_matrix.csv
├── scripts
│   └── preview_data.py
├── src
│   └── patched
│       ├── __init__.py
│       ├── data_load.py
│       ├── heat_map.py
│       ├── lat_long.py
│       ├── paths.py
│       └── spotify_comm.py
├── tests
│   └── test_app.py
├── web
│   ├── outputs
│   │   └── heatmap.html
│   └── templates
│       └── patched.html
└── main.py
```

- Application code lives under `src/patched` and is exposed as a package.
- Datasets are grouped into `data/raw` and `data/processed`.
- Generated site assets live in `web/outputs`, while static templates live in `web/templates`.
- Utility scripts and tests sit under `scripts/` and `tests/` respectively.
