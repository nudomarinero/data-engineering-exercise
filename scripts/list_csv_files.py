from itertools import product

for year, month in product(range(2009, 2021), range(1,13)):
    print(f"https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_{year}-{month:02d}.csv")