"""End-to-end tests"""
import hashlib
from io import StringIO
from pathlib import Path
import pytest
from dataeng import pipeline


BASE_DIR = Path(__file__).resolve().parents[1]
TEST_STORAGE_PATH = Path(BASE_DIR, "tests", "data")
CSV_2014 = TEST_STORAGE_PATH / Path("yellow_tripdata_2014-08-small.csv")
CSV_2020 = TEST_STORAGE_PATH / Path("yellow_tripdata_2020-01-small.csv")
CSV_2009 = TEST_STORAGE_PATH / Path("yellow_tripdata_2009-09-small.csv")


# MD5 equivalent to run "poetry run compute_yellow tests/data/yellow_tripdata_2020-01-small.csv | md5sum"
TEST_PARAMS_LOCAL = [
    (CSV_2009, 0.9, "b0a089b0c4a990793616a7f82e5c72fe"),
    (CSV_2014, 0.9, "a59610072a0407e4d4bdbfb3e4eb648a"),
    (CSV_2020, 0.9, "cc3be2476b81fd3da2cf438b0af228c0"),
]


@pytest.mark.parametrize("input_file, quantile, output_md5", TEST_PARAMS_LOCAL)
def test_similar_output_file(input_file, quantile, output_md5):
    out_buffer = StringIO()
    pipeline(input_file, quantile=quantile, output=out_buffer)
    md5 = hashlib.md5(out_buffer.getvalue().encode('utf-8'))
    assert output_md5 == md5.hexdigest()


TEST_PARAMS_URL = [
    ("https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2009-09.csv", 0.9, "93b3d26ed12bac86f50e70b1fe963572"),
    ("https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2014-08.csv", 0.9, "f0716ca12b8ba3551a190fd42e163a14"),
    ("https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-01.csv", 0.9, "cc3be2476b81fd3da2cf438b0af228c0"),
]


@pytest.mark.webtest
@pytest.mark.parametrize("input_file, quantile, output_md5", TEST_PARAMS_URL)
def test_similar_output_url(input_file, quantile, output_md5):
    out_buffer = StringIO()
    pipeline(input_file, quantile=quantile, output=out_buffer)
    md5 = hashlib.md5(out_buffer.getvalue().encode('utf-8'))
    assert output_md5 == md5.hexdigest()
