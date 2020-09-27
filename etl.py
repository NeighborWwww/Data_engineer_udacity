import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''--input:
        cur: the cursor, can execute the insert queries

        filepath: the filepath of the log dataset. the program will load the .json files in this path and
        load the information into pandas dataframe.

      --output:
        void function. all the queries will be execute inside the function.

    The function load the json files in the given filepath and transform them as dataframe. 
    then, reconstruct the data and using insert queries to load data into 
    database (artists table and songs table). '''

    #extract data from json file
    df = pd.DataFrame(columns = pd.read_json(filepath[0],lines = True).columns)
    for record in filepath:
        data = pd.read_json(record,lines = True)
        df = df.append(data)
        
    #transform data into the desire form
    song_data = pd.DataFrame({'song_id':df['song_id'], 'title':df['title'], \
                            'artist_id':df['artist_id'], 'year':df['year'], \
                            'duration':df['duration']})
    artist_data = pd.DataFrame({'artist_id':df['artist_id'], 'name':df['artist_name'], \
                                'location':df['artist_location'], 'latitude':df['artist_latitude'], \
                                'longtitude':df['artist_longitude']})

    #load the data into the table
    for i, row in song_data.iterrows():

        cur.execute(song_table_insert, list(row))
    
    # insert artist record
    for i, row in song_data.iterrows():

        cur.execute(artist_table_insert, list(row))


def process_log_file(cur, filepath):
    '''--input:
        cur: the cursor, can execute the insert queries

        filepath: the filepath of the songfile dataset. the program will load the .json files in 
        this path and load the information into pandas dataframe.

       --output:
        void function. all the queries will be execute inside the function.

    The function load the json files in the given filepath and transform them as dataframe. 'page' = NextSong 
    need to be filtering out. then, reconstruct the data and using insert queries to load data into database 
    (time table and users table). select the data from the dimension table, reconstruct the data, and insert 
    desired data into fact table (songplay table). '''
    # extract data from json file
    df = pd.DataFrame(columns = pd.read_json(filepath[0],lines = True).columns)
    
    for file in filepath:    
        data = pd.read_json(file, lines = True)
        df = df.append(data)

    #transform data into the desire form
    dt = df[df['page'] == 'NextSong']
    t = dt['ts']
    date = pd.to_datetime(t, unit = 'ms')
    time_df = pd.DataFrame({'start_time':date,'hour':date.dt.hour,'day':date.dt.day, \
                            'week':date.dt.week,'month':date.dt.month,'year':date.dt.year, \
                            'weekday':date.dt.weekday})

    user_df = pd.DataFrame({'user_id':df['userId'],'first_name':df['firstName'], \
                            'last_name':df['lastName'],'gender':df['gender'], \
                            'level':df['level']})

    #load the data into the tables

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))


    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts,unit = 'ms'), \
                                        row.userId, row.level, songid, artistid, row.sessionId)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''--input: 
            cur: the cursor, can execute queries
            conn: connection, can be use to commit queries if autocommit is not apply
            filepath: the filepath of dataset
            func: the function name to call different functions
       --output:
            void function

        the function can find each json file path in the directory given, and run the function provided above '''
        
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))


    func(cur, all_files)



def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    conn.set_session(autocommit = True)

    process_data(cur, conn, filepath='./data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='./data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()