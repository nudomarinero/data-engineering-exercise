from pathlib import Path
import numpy as np
import numpy.testing as nt
from dataeng import Extractor, location_type, load_header_url, load_header_file


# Some base data to compare in the tests
BASE_DIR = Path(__file__).resolve().parents[1]
TEST_STORAGE_PATH = Path(BASE_DIR, "tests", "data")
CSV1 = TEST_STORAGE_PATH / Path("yellow_tripdata_2014-08-small.csv")
CSV2 = TEST_STORAGE_PATH / Path("yellow_tripdata_2020-01-small.csv")
CSV3 = TEST_STORAGE_PATH / Path("yellow_tripdata_2009-09-small.csv")
CSV1_HEADER = "vendor_id, pickup_datetime, dropoff_datetime, passenger_count, trip_distance, pickup_longitude, pickup_latitude, rate_code, store_and_fwd_flag, dropoff_longitude, dropoff_latitude, payment_type, fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount"
CSV2_HEADER = "VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge"
DIST1 = np.array([2.7000000000000002, 20.399999999999999, 2.1000000000000001, 1.3, 1.7, 1.7, 1, 9.1999999999999993, 2.6000000000000001, 1.3999999999999999, 3.2000000000000002, 7.7999999999999998, 1.1000000000000001, 3.2999999999999998, 5.2999999999999998, 6.2000000000000002, 15.6,  0.90000000000000002, 1.3999999999999999])
DIST2 = np.array([1.20, 1.20, .60, .80, .00, .03, .00, .00, .00, .70, 2.40, .80, 3.30, 1.07, 7.76, 1.60, .50, 1.70, 8.45, .00])
DIST3 = np.array([10.23,  0.62,  0.96,  4.25,  0.99,  1.78,  2.16,  3.38,  7.75, 4.46,  3.13,  0.68,  4.5 ,  1.83,  1.53,  0.76,  4.83,  1.28])
URL_CSV1 = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2014-08.csv"
URL_CSV2 = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2020-01.csv"


def test_load_local_csvs():
    Extractor(CSV1)
    Extractor(CSV2)

def test_retrieve_trip_distance_column_format1():
    """This format required the stripping of the header column names"""
    result = Extractor(CSV1, check_columns=["trip_distance"]).data
    nt.assert_array_equal(result["trip_distance"], DIST1)

def test_retrieve_trip_distance_column_format2():
    """This format is OK"""
    result = Extractor(CSV2, check_columns=["trip_distance"]).data
    nt.assert_array_equal(result["trip_distance"], DIST2)

def test_retrieve_trip_distance_column_format3():
    """This format required converting to lower case the header column names"""
    result = Extractor(CSV3, check_columns=["trip_distance"]).data
    nt.assert_array_equal(result["Trip_Distance"], DIST3)


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




