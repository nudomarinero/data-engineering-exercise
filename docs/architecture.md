# Architecture Decision Records

This is a very simplified version of an ADR to explain the rationale under some decisions made to implement the solution to the problem.

TODO. Add:
* Pipeline structure
* Use of intermediate caching
* Testing framework
* Continuous Integration environment

## Reproducibility

We would like to be able to easily reproduce the proposed solution (the processing pipeline). 

### Context

* The pipeline should be fully reproducible by any developer interested. 
* Problems with dependencies and unwanted interactions with the local environment should be curtailed from the beginning.

### Decision

We will use **Poetry** to be able to isolate the environment and reproduce the dependencies. It is a tool that would be easy to install for any developer and that solves a lot of trouble by pinning the different versions of the dependencies. It can also be easily integrated in CI pipelines and in containers.

If we need to completely isolate the environment we will use a **Docker container**. Docker is well known to developers and would allow the complete reproduction of the environment even in tricky systems setups. It will also open the possibility to release the processing pipeline as a micro-service. Apart from the flexibility in term of any future release of the processing pipeline, it would also allow to test the moving of the computing load to the data location in order to measure the performance improvement.

### Consequences and future

Once the dependency on Poetry is entered, it may be difficult (but not impossible) to go back to a simpler solution. 


## Working storage of data

Where would the data be stored (Load and Transform steps)?

### Context

* The data fits in memory.
* The time to get a solution to the problem is very limited and future extension to more general cases is unlikely as this is just an exercise.

### Decision

Data will be loaded and processed in memory.

We will use **[astropy.table](https://docs.astropy.org/en/stable/table/index.html)** to load the data in memory. The data will be loaded as an numpy structured array (with some additions) which will allow to perform quick optimized operations on them. The library offers these additional features:
* The structure of the data can be guessed automatically.
* Typical errors in CSV files (headers with non-trimmed white spaces, empty rows...) can be automatically corrected.
* Memory mapping to lazily load data.
* Output of data in custom formats.
* Possibility to load data directly from URLs.

### Consequences and future

This decision is likely to allow to deliver a working solution in time.

The use of `astropy.table` also helps with the validation of data and the performance.

In the future, if the data does not fit in memory a different solution would be needed. A column-oriented database would be ideal in this case. This change would require a full change in the architecture of the solution.
