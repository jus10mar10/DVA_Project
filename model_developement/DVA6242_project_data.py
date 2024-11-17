import pandas as pd
import requests
import sqlite3
import os

# New SQLlite db if it doesn't exist already
db_filename = 'openf1_data.db'

def fetch_dataframes(endpoints, db_filename):
    # Connect to SQLite db
    conn = sqlite3.connect(db_filename)
    dataframes = {}
    for name, info in endpoints.items():
        table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}';"
        table_exists = pd.read_sql_query(table_exists_query, conn)

        if not table_exists.empty:
            # If table exists in db, load the data from SQLite
            print(f"Loading '{name}' data from SQLite db")
            dataframes[name] = pd.read_sql_query(f"SELECT * FROM {name}", conn)
        else:
            # Otherwise, get data from the API
            print(f"Getting '{name}' data from F1 API")
            url = info['url']
            params = info.get('params')  # Optional parameters

            try:
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data)

                date_columns = ['date', 'date_start', 'date_end']
                # Convert Date columns to date time
                for col in date_columns:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], format='ISO8601', errors='coerce')

                    # Save df to SQLite db
                    df.to_sql(name, conn, if_exists='replace', index=False)
                    dataframes[name] = df
                    print(f"Saved '{name}' data to SQLite db")
                else:
                    print(f"Failed to get data for '{name}': {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error while fetching data for '{name}': {e}")

    conn.close()
    return dataframes

# Define the URLs/APIs
endpoints = {
    'stints': {
        'url': 'https://api.openf1.org/v1/stints',
        # columns: ['meeting_key', 'session_key', 'stint_number', 'driver_number', 'lap_start', 'lap_end', 'compound', 'tyre_age_at_start']
    }, 
    'weather': {
        'url': 'https://api.openf1.org/v1/weather',
        # columns: ['air_temperature', 'date', 'humidity', 'meeting_key', 'pressure', 'rainfall', 'session_key', \
        # 'track_temperature', 'wind_direction', 'wind_speed']
    },
    'pit': {
        'url': 'https://api.openf1.org/v1/pit',
        # columns: ['date', 'driver_number', 'lap_number', 'meeting_key', 'pit_duration', 'session_key']
    },
    'car_data': {
        'url': 'https://api.openf1.org/v1/car_data', # Timing out right now...
        # columns: ['brake', 'date', 'driver_number', 'drs', 'meeting_key', 'n_gear', 'rpm', 'session_key', 'speed', 'throttle']
    },
    'meetings': {
        'url': 'https://api.openf1.org/v1/meetings',
        # columns: ['circuit_key', 'circuit_short_name', 'country_code', 'country_key', 'country_name', 'date_start',\
        # 'gmt_offset', 'location', 'meeting_key', 'meeting_name', 'meeting_official_name', 'year']
    },
    'sessions': {
        'url': 'https://api.openf1.org/v1/sessions',
        # columns: ['circuit_key', 'circuit_short_name', 'country_code', 'country_key', 'country_name', 'date_end',\
        #  'date_start', 'gmt_offset', 'location', 'meeting_key', 'session_key', 'session_name', 'session_type', 'year']
    },
    'laps': {
        'url': 'https://api.openf1.org/v1/laps',
        # columns: ['date_start', 'driver_number', 'duration_sector_1', 'duration_sector_2', 'duration_sector_3', 'i1_speed',\
        #  'i2_speed', 'is_pit_out_lap', 'lap_duration', 'lap_number', 'meeting_key', 'segments_sector_1', 'segments_sector_2',\
        #  'segments_sector_3', 'session_key', 'st_speed']
    }
}

# Get data from API or SQLite database
dataframes = fetch_dataframes(endpoints, db_filename)

# # df samples
# for name, df in dataframes.items():
#     print(f"\n{name} DataFrame:")
#     print(df.head())

