Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.

The goal is to analysis the user listening habit and taste. The platform can learn the user interests in style of music (assume we have a seperate style table related with song table) or artists using this data. The service provider can provide the music which are more related to the taste of each user


State and justify your database schema design and ETL pipeline.

Star schema is used in this application. Songplay table is set as the fact table, contained with user data and songs data and something else useful information. users, songs, artists, time as the dimension table. There are two source of data need to be pip in. The song data and the user login data are in seperate path. The data in song data has been processed to the songs and artists table. The artistID and songID as a foreign key in the fact table. The data in user login data has been processed to the users and time. The userID and the timestamp as foreign key in the fact table.
