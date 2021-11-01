# Data Engineering Exercise

![Tests status](https://github.com/nudomarinero/data-engineering-exercise/actions/workflows/tests.yml/badge.svg)

Data Engineering Exercise

The problem to solve would be: "Using [NYC “Yellow Taxi” Trips Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page), return all the trips over 90 percentile in distance traveled for any of the CSV files you can find there."

Context about the problem to solve:
* The data are probably dirty and inconsistent.
* Data are stored as objects in S3.
* As the problem is described, we would work on individual data sets that correspond to one month of data and, crucially, fit in memory.
* The time to implement a system processing all these data is limited to a few hours.

Given the previous constrains, we will follow the following strategy. A first exploration of the data will allow us to know how dirty they are, but validation will also be implemented in the first steps of the processing to try to catch as many problems as possible as early as possible. The structure of the pipeline would be similar to an EtLT (Extract, transform, Load, Transform) schema but customized for the problem.

As a first approximation we would need to load ("extract") the data from their location

* It should be possible to load data from a local CSV or directly using the URL.

The data are loaded in memory in a structured Numpy array. Computations on this kind of array are relatively straight forward. We will make use of the [quantile](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html) algorithm already implemented in Numpy and the indexing properties to retrieve the relevant data.


TODO:
* Extend rationale
* Add logging
## Installation

The requirements to run this project are:
* [git](https://git-scm.com/)
* Python 3.7 or higher
* [Poetry](https://python-poetry.org/)

### With Poetry

The test pipeline can be installed using [Poetry](https://python-poetry.org/) which will allow the creation of a reproducible isolated environment.

Although Poetry is a Python package, it is recommended to be installed isolated from any local Python environment. This can be achieved with the following command as explained in their [web page](https://python-poetry.org/docs/#installation):
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

Once Poetry is [installed](https://python-poetry.org/docs/#installation), the project can be installed locally with:
```bash
poetry install
```

## Usage

Run the pipeline with:
```bash
poetry run compute_yellow <URL_OR_FILE>
```

For example:
```bash
poetry run compute_yellow https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-01.csv
```
## Tests and profiling

Run the tests with:
```bash
poetry run pytest
```

The tests are run as part of the CI framework based on Github Actions.

To profile the CPU and memory usage of the pipeline we can use [psrecord](https://github.com/astrofrog/psrecord) which is installed by default as part of the development dependencies. For example:
```bash
poetry run psrecord "poetry run compute_yellow tests/data/yellow_tripdata_2020-01.csv" --log activity.txt
# the following command will produce a plot
poetry run psrecord "poetry run compute_yellow tests/data/yellow_tripdata_2020-01.csv" --plot plot.png
```

## Future development

 
