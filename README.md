# ETL Music Streaming app
In this repository, there are to example of an ETL pipeline and Database design either in PostgreSQL and Cassandra. Each folder contains the code and data necessary to create and populate the database.

# Files/Folders in this repository


* **[PostgreSQL](PostgreSQL)**: Folder containing SQL oriented ETL pipeline.
* **[Cassandra](Cassandra)**:  Folder containing No-SQL ETL pipeline.
* **[AWS_Redshift](AWS Redshift)**:  Folder containing AWS Redshift-based ETL pipeline.


# Dataset used

The dataset used is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). Each file is in JSON/CSV format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID.
