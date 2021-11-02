from itertools import product
from pathlib import Path
import requests

# There are two formats for the S3 objects in the links. Both would retrieve the same data set but we are checking if they are all there.
csvs = {
    (
        f"https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_{year}-{month:02d}.csv",
        f"https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{year}-{month:02d}.csv"
    )
    for year, month in product(range(2009, 2021), range(1,13))
}

URL = "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"

page = requests.get(URL, stream=True).content.decode('utf8')
found = {csv for csv in csvs if csv[0] in page or csv[1] in page}

print("Not found:")
print(csvs - found)
