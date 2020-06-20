import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Process song files and index them in the artists and songs tables.

        Args:
            cur (Cursor.object): Cursor to the database.
            filepath (str): Path to .json file.


        Examples:
            Given a DB cursor and a json path:

            >>> conn = psycopg2.connect("host=127.0.0.1 dbname=dbname user=user password=password")
            >>> cur = conn.cursor()
            >>> process_song_file(cursor, '/path/to/file.json')
            >>> conn.commit()

    """
        
    # open song file
    df = pd.read_json(filepath, lines=True)
    
    # insert song record
    song_data = df.loc[:, ['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.loc[:, ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Process log files and insert the data in the time, users, songplays tables.

        Args:
            cur (Cursor.object): Cursor to the database.
            filepath (str): Path to .json file.


        Examples:
            Given a DB cursor and a json path:

            >>> conn = psycopg2.connect("host=127.0.0.1 dbname=dbname user=user password=password")
            >>> cur = conn.cursor()
            >>> process_log_file(cur, '/path/to/file.json')
            >>> conn.commit()

    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df.page == 'NextSong', :]

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts)
    
    # insert time data records
    time_data = [df.ts.values, t.dt.hour.values, t.dt.day.values, t.dt.weekofyear.values, t.dt.month.values, t.dt.year.values, t.dt.dayofweek.values]
    column_labels = ['timestamp', 'hour', 'day', 'week','month','year','weekeday'] 
    time_df = pd.DataFrame(time_data, index=column_labels).T

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:, ['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates().reset_index(drop=True)

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
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Wrapper function around the two process data functions for songs and logs.

    Args:
        cur (Cursor.object): Cursor to the database.
        conn (Connection.object): Connection to database
        filepath (str): Path to .json file.
        func (Function): function to process and import the data contained in filepath.


    Examples:
        Given a DB cursor and a json path:

        >>> conn = psycopg2.connect("host=127.0.0.1 dbname=dbname user=user password=password")
        >>> cur = conn.cursor()

        >>> process_data(cur, conn, '/path/to/file.json', process_song_file)

    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()