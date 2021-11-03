"""Module with heuristical transformation recipes for the data"""


HEADER_TRANSLATION_FORMAT2009 = {
    "vendor_name": "vendor_id",
    "Trip_Pickup_DateTime": "pickup_datetime",
    "Trip_Dropoff_DateTime": "dropoff_datetime",
    "Passenger_Count": "passenger_count",
    "Trip_Distance": "trip_distance",
    "Start_Lon": "pickup_longitude",
    "Start_Lat": "pickup_latitude",
    "Rate_Code": "rate_code",
    "store_and_forward": "store_and_fwd_flag",
    "End_Lon": "dropoff_longitude",
    "End_Lat": "dropoff_latitude",
    "Payment_Type": "payment_type",
    "Fare_Amt": "fare_amount",
    "surcharge": "surcharge",  #
    "mta_tax": "mta_tax",  #
    "Tip_Amt": "tip_amount",
    "Tolls_Amt": "tolls_amount",
    "Total_Amt": "total_amount"
}


HEADER_TRANSLATION_FORMAT2020 = {
    "VendorID": "vendor_id",
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
    "passenger_count": "passenger_count",  #
    "trip_distance": "trip_distance",  #
#    "Start_Lon": "pickup_longitude",  # Not found, changed to ref. to table PULocationID
#    "Start_Lat": "pickup_latitude",  # Not found, changed to ref. to table PULocationID
    "RatecodeID": "rate_code",
    "store_and_fwd_flag": "store_and_fwd_flag",  #
#    "End_Lon": "dropoff_longitude",  # Not found, changed to ref. to table DOLocationID
#    "End_Lat": "dropoff_latitude",  # Not found, changed to ref. to table DOLocationID
    "PULocationID": "PULocationID",  # New column with ref. to additional table
    "DOLocationID": "DOLocationID",  # New column with ref. to additional table
    "payment_type": "payment_type",  #
    "fare_amount": "fare_amount",  #
    "extra": "surcharge",  # TODO: CHECK equivalence
    "mta_tax": "mta_tax",  #
    "tip_amount": "tip_amount",  #
    "tolls_amount": "tolls_amount",  #
    "improvement_surcharge": "improvement_surcharge",  # New column
    "total_amount": "total_amount",  #
    "congestion_surcharge": "congestion_surcharge"  # New column
}

MISSING_COLS2020 = {
    "pickup_longitude", 
    "pickup_latitude", 
    "dropoff_longitude", 
    "dropoff_latitude"
    }


# Heuristic to match column id with format
FORMAT_IDS = {
    "vendor_name": HEADER_TRANSLATION_FORMAT2009,
    "VendorID": HEADER_TRANSLATION_FORMAT2020
}