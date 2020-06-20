# Summary

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like to create a Postgres database with tables designed to optimize queries on song play analysis.The aim is to create a database schema and ETL pipeline for this analysis.

# How to run the ETL pipeline

To create the database tables and run the ETL pipeline, you need to run the following two files in the following order:

To create tables:
```bash
python create_tables.py
```
To fill tables via ETL:
```bash
python etl.py
```

# Files/Folders in this repository


* **[data](data)**: Folder containing songs and logs data. They are stored in .json format
* **[create_tables.py](create_tables.py)**: Python script to perform postgreSQL commands for creation/reset of the database and tables.
* **[sql_queries.py](sql_queries.py)**: Python script containing postgreSQL commands used by create_tables.py and etl.py
* **[etl.py](etl.py)**: Python script to extract the information from Song and Log data within the **[data](data)** folder and inserting them to the database and tables.

# Objective

Storing data in a database makes it easier for ad-hoc analysis. Using postgreSQL and the star scheme, joins and aggregations allows Analyst to query and access data in a comprehensive manner. By using relational databases, Sparkify can access and extract valuable information from it user logs. 

# The database schema design and ETL pipeline.

Here, a Relational Database Schema was created to enable Sparkify to analyze their data. This database was then populated with an ETL pipeline.

The star scheme enables the company to view the user behaviour over several dimensions.
The fact table is used to store all user song activities that contain the category "NextSong". Using this table, the company can relate and analyze the different dimensions of this schema: users, songs, artists and time.

In order to populate the relational database, an ETL pipeline was used. The ETL pipeline made possible to extract the relevant information from the log files of the user behaviour as well as the corresponding data from the songs and load it into the schema.

* **Fact Table**: songplays
* **Dimension Tables**: users, songs, artists and time.

# Dataset used

The first dataset is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.
