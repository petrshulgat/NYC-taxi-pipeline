import os
from dotenv import load_dotenv

load_dotenv()

PG_USER = os.getenv("POSTGRES_USER", "nyc_user")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "nyc_pass")
PG_DB = os.getenv("POSTGRES_DB", "nyc_taxi")
PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
PG_PORT = os.getenv("POSTGRES_PORT", "5432")

NYC_YEAR = os.getenv("nyc_year", "2026")
NYC_MONTH = os.getenv("nyc_month", "01")

PARQUET_URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{NYC_YEAR}-{NYC_MONTH}.parquet"

LOCAL_RAW = f"D:/study/Data_Engineering/NYC-taxi-pipeline/data/raw/yellow_tripdata_{NYC_YEAR}-{NYC_MONTH}.parquet"

