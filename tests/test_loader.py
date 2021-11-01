from pathlib import Path
import numpy as np
import numpy.testing as nt
from dataeng import Loader, location_type, load_header_url, load_header_file


# Some base data to compare in the tests
BASE_DIR = Path(__file__).resolve().parents[1]
TEST_STORAGE_PATH = Path(BASE_DIR, "tests", "data")
CSV1 = TEST_STORAGE_PATH / Path("yellow_tripdata_2014-08-small.csv")
CSV2 = TEST_STORAGE_PATH / Path("yellow_tripdata_2020-01-small.csv")
CSV1_HEADER = "vendor_id, pickup_datetime, dropoff_datetime, passenger_count, trip_distance, pickup_longitude, pickup_latitude, rate_code, store_and_fwd_flag, dropoff_longitude, dropoff_latitude, payment_type, fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount"
CSV2_HEADER = "VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge"
DIST1 = np.array([2.7000000000000002, 20.399999999999999, 2.1000000000000001, 1.3, 1.7, 1.7, 1, 9.1999999999999993, 2.6000000000000001, 1.3999999999999999, 3.2000000000000002, 7.7999999999999998, 1.1000000000000001, 3.2999999999999998, 5.2999999999999998, 6.2000000000000002, 15.6,  0.90000000000000002, 1.3999999999999999])
DIST2 = np.array([1.20, 1.20, .60, .80, .00, .03, .00, .00, .00, .70, 2.40, .80, 3.30, 1.07, 7.76, 1.60, .50, 1.70, 8.45, .00])
URL_CSV1 = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2014-08.csv"
URL_CSV2 = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2020-01.csv"


def test_load_local_csvs():
    Loader(CSV1)
    Loader(CSV2)

def test_retrieve_trip_distance_column():
    result1 = Loader(CSV1, columns=["trip_distance"]).data
    result2 = Loader(CSV2, columns=["trip_distance"]).data
    nt.assert_array_equal(result1["trip_distance"], DIST1)
    nt.assert_array_equal(result2["trip_distance"], DIST2)

def test_location_type_url():
    assert location_type(URL_CSV1) == "url"

def test_location_type_local_file():
    assert location_type(str(CSV1)) == "file"

def test_location_type_local_file_not_existing():
    assert location_type("dummy.file") == "unknown"

def test_load_header_url():
    assert load_header_url(URL_CSV1)[0] == CSV1_HEADER
    assert load_header_url(URL_CSV2)[0] == CSV2_HEADER

def test_load_header_file():
    assert load_header_file(CSV1)[0] == CSV1_HEADER
    assert load_header_file(CSV2)[0] == CSV2_HEADER

# Test errors with malformed data.




