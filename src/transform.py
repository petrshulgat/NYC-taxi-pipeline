import polars as pl
import pandas as pd

def clean(path):

    pl_df = pl.read_parquet(path)
    df = pl_df.to_pandas()

    rename_map = {
        "VendorID" : "vendor_id",
        "RatecodeID" : "ratecode_id",
        "PULocationID" : "pu_location_id",
        "DOLocationID" : "do_location_id"
    }

    df = df.rename(columns=rename_map)

    df = df[(df["tpep_dropoff_datetime"] > df["tpep_pickup_datetime"]) &
            (df["trip_distance"] > 0) &
            (df["total_amount"].notna())].copy()

    duration = df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    df["duration_min"] = (duration.dt.total_seconds() / 60).round().astype("int64")

    keep = ["vendor_id", "tpep_pickup_datetime", "tpep_dropoff_datetime",
            "trip_distance", "fare_amount", "tip_amount", "total_amount",
            "pu_location_id", "do_location_id", "duration_min"]

    clean_df = df[keep].copy().rename(columns={
        "tpep_pickup_datetime" : "pickup_ts",
        "tpep_dropoff_datetime" : "dropoff_ts"
    }) 

    return clean_df
    

