CREATE Table if NOT EXISTS raw_trips(
    vendor_id INT,  
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance FLOAT,
    ratecode_id INT,
    store_and_fwd_flag STRING,
    pu_location_id INT,
    do_location_id INT,
    payment_type INT,
    fare_amount FLOAT,
    extra FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    improvement_surcharge FLOAT,
    total_amount FLOAT,
    improvement_surcharge FLOAT,
    airport_fee FLOAT,
    cbd_congestion_fee FLOAT
);


CREATE Table IF NOT EXISTS clean_trips(
    vendor_id INT,
    pickup_ts TIMESTAMP,
    dropoff_ts TIMESTAMP,
    trip_distance FLOAT,
    fare_amount FLOAT,
    tip_amount FLOAT,
    total_amount FLOAT,
    pu_location_id INT,
    do_location_id INT
)