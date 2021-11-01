# data-engineer-exercise

![Tests status](https://github.com/nudomarinero/data-engineer-exercise/actions/workflows/tests.yml/badge.svg)

Data Engineer Exercise

Currently, it only computes the quantile for the travelled distance of some of the  NYC "Yellow Taxi" Trips datasets.

TODO:
* Add rationale
* Add logging
* Remove download clutter from the Loader
* Add docs
## Installation

The tool can be installed using Poetry which will allow the creation of a reproducible isolated environment.

```bash
poetry install
```

## Usage

Run the pipeline with:
```bash
poetry run compute_yellow <URL>
```

For example:
```bash
poetry run compute_yellow https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-01.csv
```
## Run the tests

Run the tests with:
```bash
poetry run pytest
```

## Future development

 
