# PURPOSE:
The purpose of this is to implement and ETL process that fill a subset of tables that were derived from two different sources.

## Source Files
The soource files are located on the /data directory
    
1. ```song_data``` Song Details: Artist and Song specific details 
2. ```log_data```  Log Details: User information that describes what a user has listened to during a specific time.

The ETL process is in charge of extracting the data and loading all file records into the derived tables that are used for analytics purposes. 

## Destination tables
The resulting set of tables are as it follows:

|Table Name| Table Purpose 
|---|---
| ```songplays```| Contains the details of every single time a song of a given artist has been played by a given user.
| ```users```| Contains the users detail information
| ```songs```| Contains the songs detail information
| ```artists```| Contains the artists information
| ```time```| Contains some derived time elements that facilitate further analysis for the ```songplays``` fact table linked to the timestamp


## Schema
The schema used in this project consists of one Fact Table ```songplays``` and four different dimension tables ```users, songs, artist, time```

### Fact Table
1. ```songplays``` table has columns 
   _songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent_

### Dimension Tables
1. ```users``` table has columns 
   _user_id, first_name, last_name, gender, level_
2. ```songs``` table has columns 
   _song_id, title, artist_id, year, duration_
3. ```artists``` table has columns 
   _artist_id, name, location, latitude, longitude_
4. ```time``` table has columns 
   _start_time, hour, day, week, month, year, weekday_
 


## Project Components
There are a set of file that are used in this project 

* ```slq_queries.py``` --> Contains the content to DROP and CREATE tables, INSERT INTO tables, and SELECT records from the SONGS and ARTIST tables.

* ```create_tables.py```--> Contains the code that is used to trigger the initialization of the project. It references the schema defined on the ```slq_qyeries.py```

* ```test.ipnyb``` -> It is a Jupiter notebook that is used to check if the ETL process run by ```etl.py``` and ```etl.ipynb``` works as it returns a subset of data for each table.

* ```etl.ipynb``` -> It is a Jupiter notebook that was used to document and create the code to be populated on the ```etl.py``` script.

* ```etl.py``` -> Contains the code that is used to define the ETL process needed to process all the files that reside on the ```/data``` subdirectories.


## Sample Queries
The following queries can be used to determine the number of records that exists in each table
```SQL 
SELECT COUNT(*) FROM songplays;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM songs;
SELECT COUNT(*) FROM artists;
SELECT COUNT(*) FROM time;
```

You can also get all the details for a given user (in the example below)
```SQL
    SELECT u.first_name 
         , u.last_name 
         , count(s.*) Number_Of_Songs_Played 
    FROM users u 
    JOIN songplays s 
        ON s.user_id = u.user_id 
    WHERE u.first_name = 'Connar' 
    GROUP BY u.first_name 
            , u.last_name;
    
```

**NOTE** The queries above have been added to the ```test.ipnyb``` for validation purposes.

## How to run the Project Scripts 
In order to test this project, you need to run the following <br>
```run create_tables.py```

Then once the command above is complete, you can run the following to load all the files that are on the subdirectory ```\data``` <br>
```run etl.py```

Once those two scripts are run, you can proceed to test the data with the ```test.ipynb``` notebook.