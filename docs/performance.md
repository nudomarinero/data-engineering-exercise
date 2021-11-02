# Performance

The main performance penalty in the current project is in the extraction of the data. The time used in retrieving the data from S3 is about 5 times higher than the time spent loading the data into memory and performing the computation. Without using intermediate storage (a column-oriented database) this is the bottleneck for the processing. This should be the first point to tackle if the system were to be extended and used in production.

The other big performance penalty comes in terms of developer time with respect to computing time in a system that is only meant to be a test. Part of this overhead is spent in understanding how dirty is the data, what are the real requirements of the product, and implementing robust pipeline steps and tests. Fortunately, this overhead tends to diminish as the system is developed and used in continuous production, but this should be considered when developing a real product. 

## Extraction step

If some columns are known to not to be useful they can be ignored by the process that loads them into memory. 

In some tests the performance increased by up to 100% if the number of columns was limited to a pair of them (useful only in a few specific cases)