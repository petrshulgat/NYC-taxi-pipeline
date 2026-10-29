# NYC Taxi ETL Pipeline

A small end-to-end data pipeline: it downloads one month of NYC Yellow Taxi trip data, cleans it, and loads it into Postgres.

## How it works

```
NYC TLC parquet file (public, monthly)
        │
   [Extract]    download file -> data/raw/
        │
   [Load raw]   append to trips_raw   (near-source schema)
        │
   [Transform]  clean rows, add duration_min and distance_mi
        │
   [Load clean] append to trips_clean (curated table)
```

Two tables on purpose:
- `trips_raw` keeps the source data close to original, so you can reprocess later.
- `trips_clean` holds only validated rows and the columns needed for analytics.

## Project structure

```
├─ docker-compose.yml     # Postgres
├─ .env.example           # config template, copy to .env
├─ requirements.txt
├─ sql/
│  └─ schema.sql          # creates trips_raw and trips_clean
├─ src/
│  ├─ settings.py         # reads .env, builds download URL and file path
│  ├─ db.py               # SQLAlchemy engine for Postgres
│  ├─ extract.py          # downloads the parquet file
│  ├─ transform.py        # renames columns, filters bad rows, derives columns
│  ├─ load.py             # chunked inserts into Postgres
│  └─ etl_flow.py         # runs extract -> load raw -> transform -> load clean
└─ data/raw/              # downloaded files
```

## What each file does

| File | Role |
|---|---|
| `settings.py` | Loads `.env`. Builds the URL and local path from `NYC_YEAR` and `NYC_MONTH`. |
| `db.py` | Creates the Postgres connection engine used by the loader. |
| `extract.py` | Streams the parquet file from the TLC site to `data/raw/` in small chunks. |
| `transform.py` | Reads parquet with Polars, renames columns to snake_case, drops impossible rows (dropoff before pickup, negative distance, missing total), adds `duration_min` and `distance_mi`, keeps the analytics columns. |
| `load.py` | Aligns columns to the table schema, then inserts in chunks that stay under Postgres' 65,535-parameter limit. |
| `etl_flow.py` | Entry point. Calls the steps in order. |

## Requirements

- Python 3.13 (3.12 also works)
- Docker Desktop

## Run it (Windows PowerShell)

**1. Install dependencies**
```powershell
pip install -r requirements.txt
```

**2. Create your config**
```powershell
copy .env.example .env
```
Default values work for a local run:
```
POSTGRES_USER=nyc_user
POSTGRES_PASSWORD=nyc_pass
POSTGRES_DB=nyc_taxi
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
NYC_YEAR=2023
NYC_MONTH=01
```
Use `POSTGRES_HOST=localhost` when running Python on your machine, and `postgres` when the code runs inside Docker.

**3. Start Postgres**
```powershell
docker compose up -d
```

**4. Create the tables**
```powershell
docker exec -i nyc_pg psql -U nyc_user -d nyc_taxi < sql\schema.sql
```
Check they exist:
```powershell
docker exec -it nyc_pg psql -U nyc_user -d nyc_taxi -c "\dt"
```

**5. Run the ETL**
```powershell
python -m src.etl_flow
```

**6. Check the data**
```powershell
docker exec -it nyc_pg psql -U nyc_user -d nyc_taxi -c "SELECT COUNT(*) FROM trips_raw;"
docker exec -it nyc_pg psql -U nyc_user -d nyc_taxi -c "SELECT COUNT(*) FROM trips_clean;"
```

## Data dictionary

Column meanings are in the official TLC dictionary:
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
