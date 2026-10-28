import polars as pl
import pandas as pd
from .db import pg_engine

MAX_PARAMSIZE = 60000

def safe_size(num_cols):
    return max(1000, int(MAX_PARAMSIZE / max(1, num_cols)))   #number of rows


RAW_SCHEMA = [
    "vendor_id",
    "tpep_pickup_datetime" ,
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance" ,
    "ratecode_id" ,
    "store_and_fwd_flag" ,
    "pu_location_id" ,
    "do_location_id" ,
    "payment_type" ,
    "fare_amount",
    "extra" ,
    "mta_tax" ,
    "tip_amount" ,
    "tolls_amount" ,
    "improvement_surcharge",
    "total_amount" ,
    "congestion_surcharge",
    "airport_fee" ,
    "cbd_congestion_fee" 
]

RENAME_MAP = {
    "VendorID" : "vendor_id",
    "RatecodeID" : "ratecode_id",
    "PULocationID" : "pu_location_id",
    "DOLocationID" : "do_location_id",
    "Airport_fee" : "airport_fee"
}


def align_to_raw_schema(df):

    df = df.rename(columns=RENAME_MAP)

    for col in RAW_SCHEMA:
        if col not in df.columns:
            df[col] = pd.NA 

    df = df[RAW_SCHEMA].copy()

    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    return df 


def load_raw(parquet_path):
    pl_df = pl.read_parquet(parquet_path)
    pdf = pl_df.to_pandas()
    pdf = align_to_raw_schema(pdf)

    engine = pg_engine()
    chunksz = min(safe_size(len(pdf.columns)), 2000)
    pdf.to_sql(
        "trips_raw", engine, if_exists="append", index=False, method="multi", chunksize=chunksz
    )


def load_clean(df):
    engine = pg_engine()
    chunksz = min(safe_size(len(df.columns)), 2000)
    df.to_sql(
        "trips_clean", engine, if_exists="append", index=False, method="multi", chunksize=chunksz
    )