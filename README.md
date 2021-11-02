# Data Engineering Exercise

![Tests status](https://github.com/nudomarinero/data-engineering-exercise/actions/workflows/tests.yml/badge.svg)

Data Engineering Exercise

The problem to solve would be: "Using [NYC “Yellow Taxi” Trips Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page), return all the trips over 90 percentile in distance traveled for any of the CSV files you can find there."

Preliminary considerations:
* The data are likely to be dirty and inconsistent.
* Data are stored as objects in S3.
* As the problem is described, we would work on individual data sets that correspond to one month of data.
* The size of the dataset is small enough (0.5 to 2.5 GB) to fit in memory.
* The time to develop a system to process all these data is limited to a few hours.

The aim would be to develop a pipeline that can process the Yellow Taxi trips CSV and return a clean list of distance outliers. It should work in as much CSV files as possible and produce sound results in the limited available time for development. The information about processing failures should be insightful to be able to correct and improve the system in the future.

Given the previous constrains, we will follow the following strategy. A first [exploration of the data](docs/exploration.md) will allow us to know how dirty they are. However, validation will also be implemented in the first steps of the processing to try to catch as many problems as possible as early as possible. The structure of the pipeline would be similar to an EtLT (Extract, transform, Load, Transform) schema but adapted to our problem. Data will be first "extracted" from S3, then transformed, validated and cleaned. With the data in memory we will perform the operations and output the results. The main decisions about the architecture and design are [here](docs/architecture.md).

The pipeline should be able to work on local data but also providing directly an URL. The capability to work on local data will help with testing. However, for performance reasons and robustness, the extraction, validation and loading of data into memory can also be combined by using `astropy.table` as explained [here](docs/architecture.md#Working-storage-of-data).  The data are loaded in memory in a structured Numpy array. Computations on this kind of array are relatively straight forward and we can leverage the performance and robustness of their implementation in Numpy. We will make use of the [quantile](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html) algorithm already implemented in Numpy and the indexing properties to retrieve the relevant data. The indexing in Numpy works as a memory map that avoid the unnecessary duplication of data. The data structure and schema will be modified in memory to a clean and clear one that is robust and meaningful. The data can be then written in different formats to a file output or as a data stream (via stdout or HTTP). For simplicity we will output a reduced, clean version of the CSV with the relevant data.

The performance of different approaches and designs is discussed [here](docs/performance.md). For the possible future development of the project look [here](#Future-development).

## Installation

The requirements to run this project are:
* [git](https://git-scm.com/)
* Python 3.7 or higher
* [Poetry](https://python-poetry.org/)

The project can be installed using [Poetry](https://python-poetry.org/) which will allow the creation of a reproducible isolated environment.

Although Poetry is a Python package, it is recommended to be installed isolated from any local Python environment. This can be achieved with the following command as explained in their [web page](https://python-poetry.org/docs/#installation):
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

## Getting Started

Once Poetry is [installed](https://python-poetry.org/docs/#installation), the project can be installed locally following these steps:
### 1. Clone this Repository

```
git clone https://github.com/nudomarinero/data-engineering-exercise.git
```

### 2. Navigate to the directory

```
cd data-engineering-exercise
```

### 3. Install project with Poetry

```
poetry install
```

### 4. Run the pipeline

Run the pipeline with:
```bash
poetry run compute_yellow <URL_OR_FILE>
```

For example:
```bash
poetry run compute_yellow https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-01.csv
```
## Tests and profiling

The tests can be run with:
```bash
poetry run pytest
```

The tests are also run as part of the CI framework based on Github Actions. It currently runs the tests with the versions 3.7, 3.8, 3.9, and 3.10 of Python.

The test suite can also be run locally in different versions of Python using *tox*. Just edit the `tox.ini` file to include the versions of Python that you would like to test the pipeline on. Note that the Python versions included must be available in your system. One useful way to install them isolated from the system version is to use [pyenv](https://github.com/pyenv/pyenv).

To profile the CPU and memory usage of the pipeline, we can use [psrecord](https://github.com/astrofrog/psrecord) which is installed by default as part of the development dependencies. For example:
```bash
poetry run psrecord "poetry run compute_yellow tests/data/yellow_tripdata_2020-01.csv" \
 --log activity.txt
# the following command will produce a plot
poetry run psrecord "poetry run compute_yellow tests/data/yellow_tripdata_2020-01.csv" \
 --plot plot.png
```

## Future development

* Docker and services
* Airflow
* Performance improvements
* Additional cleaning
* Service
* Output schema