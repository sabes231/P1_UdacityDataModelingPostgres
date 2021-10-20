import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description:
        This function reads the contents of a JSON file that contians the song data which can have multiple lines, retrieves a subset of data specific to the song and artist tables, and triggers the functions to insert the song_table_insert and artist_table_insert functions.
    Arguments:
        cur: the curson object
        filepath: song data file path
    Returns:
        None
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = (df[['song_id','title','artist_id','year','duration']]).values[0]    
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = (df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]).values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description:
        - This function reads the contents of a JSON file that contains the log data which can have multiple lines
        - Filters out the records that have the page = 'NextSong'
        - Converts the time variable from the filtered dataset to its own subset of records and inserts them into the time table by triggering the  time_table_insert function.
        - It will then process a subset of data related to the song_play and artist tables, and triggers the functions to insert the song_table_insert and artist_table_insert functions.
    Arguments:
        cur: the curson object
        filepath: log data file path
    Returns:
        None
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    time_data = [[i, i.hour, i.day, i.week, i.month, i.year, i.dayofweek] for i in t]
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = (df[['userId','firstName','lastName','gender','level']]).drop_duplicates()

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
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description:
        - Retrieves the details of all different files that exist on a given location
        - Prints the total number of files found
        - Calls the function passed as a paramenter and commits its execution to the DB specified on the conn variable
    Arguments:
        cur: the curson object
        conn: containst the connectivity details to the DB
        filepath: log data file path
        function: function that will be executed
    Returns:
        None
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
    """
    Description:
        - Creates a connection to the `sparkifydb` DB  
        - Runs process_data functions to process the song_files 
        - Runs process_data functions to process the log_files
        - Closes the connection
    """

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()