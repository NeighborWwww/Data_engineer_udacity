# A music database using postgresSQL


## 1. Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.

The goal is to analysis the user listening habit and taste. The platform can learn the user interests in style of music (assume we have a seperate style table related with song table) or artists using this data. The service provider can provide the music which are more related to the taste of each user.


## 2. State and justify the database schema design and ETL pipeline.

Star schema is used in this application. Songplay table is set as the fact table, contained with user data and songs data and something else useful information. users, songs, artists, time as the dimension table. 

There are two source of data need to be pip in. The song data and the user login data are in seperate path. The data in song data has been processed to the songs and artists table. The artistID and songID as a foreign key in the fact table. The data in user login data has been processed to the users and time. The userID and the timestamp as foreign key in the fact table.

* sql_queries.py

In this files, SQL queries are stored and can be used by etl.py. It including create/drop table queries, insert queries, and select query. The select query is used to pick data from the dimension table to the fact table. The table and its columns label is shown below:

```
songplays(songplay_id SERIAL PRIMARY KEY, \
						start_time timestamp, user_id varchar NOT NULL, level varchar, song_id varchar, \
						artist_id varchar, session_id int, location varchar, user_agent varchar)

users (user_id varchar PRIMARY KEY, \
					first_name varchar, last_name varchar, gender varchar, level varchar)

songs (song_id varchar PRIMARY KEY, \
					title varchar, artist_id varchar, year int, duration numeric)

artists (artist_id varchar PRIMARY KEY, \
					name varchar, location varchar, latitude numeric, longtitude numeric)

time (start_time timestamp PRIMARY KEY, \
					hour int, day int, week int, month int,year int, weekday int)
```


* etl.py

In etl.py, the data will be extracted from the json files in the date folder. There are two groups of datasets, log dataset and music dataset. The data will be transform into pandas dataframe and manipulate into the form which can fit the insert query designed in the sql_queries.py. Here is some explaination about the functions in etl.py
	```
	def process_song_file(cur, filepath):
	--input:
		cur: the cursor, can execute the insert queries
		filepath: the filepath of the songfile dataset. the program will load the .json files in 
		this path and load the information into pandas dataframe.
	--output:
		void function. all the queries will be execute inside the function.
	--function:
		The function load the json files in the given filepath and transform them as dataframe. then, 
		reconstruct the data and using insert queries to load data into database (artists table and 
		songs table).	
	```

	```
	def process_log_file(cur, filepath):
	--input:
		cur: the cursor, can execute the insert queries
		filepath: the filepath of the log dataset. the program will load the .json files in this path and
		load the information into pandas dataframe.
	--output:
		void function. all the queries will be execute inside the function.
	--function:
		The function load the json files in the given filepath and transform them as dataframe. 'page' = NextSong 
		need to be filtering out. then, reconstruct the data and using insert queries to load data into database 
		(time table and users table). select the data from the dimension table, reconstruct the data, and insert 
		desired data into fact table (songplay table).
	```
To run the code, first step is install the postgresSQL and libraries.

Install the postgres following the instructions provided by PostgresSQL website: https://www.postgresql.org/download/linux/ubuntu/
Required libraries:
```
pip install pandas
pip install psycopg2
```

Run create_table.py first to create the database and the tables needed. Then, run the etl.py to perform etl process. Using test.ipynb can test the result of etl.
```
python create_table.py
python etl.py
```
