from .extract import download_raw
from transform import clean
from load import load_clean, load_raw
from .db import execute_sql

def check_schema():
    with open("sql/schema.sql", "r") as f:
        execute_sql(f.read())


def run_etl():
    print("Checking schema ")
    check_schema()

    print("Extracting data ")
    raw_path = download_raw()

    print("Transforming data ")
    cleaned = clean(raw_path)

    print("Loading raw data ")
    load_raw(raw_path)

    print("Loading clean data ")
    load_clean(cleaned)

    print("Complete")


if __name__ == "__main__":
    run_etl()