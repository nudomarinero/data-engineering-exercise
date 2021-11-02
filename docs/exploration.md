# Preliminary exploration of the data

The [NYC “Yellow Taxi” Trips Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) is stored as CSV files in S3. 

According to the description in <https://www1.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf> the data can be also accessed from the [Open Data portal of the City of NY](https://opendata.cityofnewyork.us/) but I assume that the point of the exercise is to work on realistic data using directly the CSV files.

There is a [description of the data](https://data.cityofnewyork.us/api/views/biws-g3hs/files/eb3ccc47-317f-4b2a-8f49-5a684b0b1ecc?download=true&filename=data_dictionary_trip_records_yellow.pdf) to be found in the files but a quick look in some of the CSV headers shows that the names of the columns are inconsistent.

There are CSV data files for all the months between 2009 and 2021. We check if all of them are listed in the web page with the script `scripts/check_csv_files.py`.

