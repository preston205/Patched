# Patched

Sandbox project

## Project layout

```
data/
  processed/
    updated_data.csv
    updated_data_backup.csv
  raw/
    Locals.csv
    data.csv
    genre_matrix.csv
public/
  index.html
scripts/
  preview_data.py
src/
  patched/
    __init__.py
    data_load.py
    heat_map.py
    lat_long.py
    paths.py
    spotify_comm.py
tests/
  test_app.py
web/
  outputs/
    heatmap.html
  templates/
    patched.html
supabase/
  migrations/
    0001_init_schema.sql
main.py
vercel.json
```

- Application code lives under `src/patched` and is exposed as a package.
- Datasets are grouped into `data/raw` and `data/processed`.
- Generated site assets live in `web/outputs`, while static templates live in `web/templates`; Vercel serves the landing page from `public/index.html`.
- Utility scripts, tests, and database migrations sit inside `scripts/`, `tests/`, and `supabase/` respectively.

## Supabase/PostgreSQL setup

1. Create a Supabase project and grab your `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_KEY`.
2. Apply the initial schema via the Supabase SQL editor or CLI:
   ```bash
   supabase db push
   ```
   or run the contents of `supabase/migrations/0001_init_schema.sql` manually.
3. Enable Row Level Security in the dashboard (the migration already installs policies) and test sign-up flows for artists and venues.
4. Store your Supabase keys locally (e.g., `.env`) and in your Vercel project so the application can read/write data securely.
