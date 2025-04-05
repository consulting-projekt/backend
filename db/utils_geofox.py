from geofox_client import GtiClient
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
from parallel_pandas import ParallelPandas

# Initialize parallel pandas
ParallelPandas.initialize(n_cpu=12, disable_pr_bar=False)

file_dir = Path(__file__).resolve(strict=True).parent
data_dir = file_dir / "data_geofox"
data_departures_dir = data_dir / "departures"
service_types = ['ZUG', 'BUS']

def get_stations(client, loadFromDisk=False , doSave=True):
    if loadFromDisk:
        # load json from folder "data_geofox"
        with open(os.path.join(data_dir, "stations.json"), "r") as f:
            res = json.load(f)
        return res

    endpoint = 'listStations' 
    request = {
    "language": "de",
    "version": 59
    }

    res = client.send(endpoint, request)

    if doSave and not loadFromDisk:
        # saving json to folder "data_geofox"
        with open(os.path.join(data_dir, "stations.json"), "w") as f:
            json.dump(res, f, indent=4)

    return res

def get_departures(client, stations, filename="departures.json", loadFromDisk=False , doSave=True):
    if loadFromDisk:
        # load json from folder "data_geofox"
        with open(os.path.join(data_departures_dir, filename), "r") as f:
            res = json.load(f)
        return res
    
    # time 	GTITime Zeitpunkt, ab dem Abfahrten gesucht werden -> 03.04.2025 00:00:00
    time =   {"date": "03.04.2025", "time": "00:00"}

    # maxTimeOffset int Maximaler Zeitversatz in Minuten -> 60 * 24
    maxTimeOffset = 60 * 24

    endpoint = 'departureList' 
    request = {
    "language": "de",
    "version": 59,
    "serviceTypes": service_types,
    "stations": stations,
    "time":  time, 
    "maxList": 10000, 
    "maxTimeOffset": maxTimeOffset, 
    }

    res = client.send(endpoint, request)

    if doSave and not loadFromDisk:
        # saving json to folder "data_geofox"
        with open(os.path.join(data_departures_dir, filename), "w") as f:
            json.dump(res, f, indent=4)

    return res


def process_departure_data(departures):
    """
    Process raw departure data to extract needed information and format properly.
    Dynamically identifies the next station and arrival time by analyzing departures
    with the same line and directionId using pandas and parallel processing.
    
    Args:
        departures: List of departure dictionaries with raw data
        
    Returns:
        List of processed departure dictionaries with essential information including next stations and arrival times
    """
    print("Processing basic departure information...")
    
    # First pass: Basic processing of departures
    processed_data = []
    base_date = datetime.strptime("03.04.2025 00:00", "%d.%m.%Y %H:%M")
    
    for departure in tqdm(departures, desc="Basic processing"):
        # Extract station information
        from_station = departure['station']['combinedName']
        from_station_id = departure['station']['id']
        
        # Line information
        line_id = departure['line']['id']
        line_name = departure['line']['name']
        line_info = departure['line']['type']['longInfo']
        direction = departure['line']['direction']
        direction_id = departure['directionId']
        
        # Calculate departure time
        time_offset = departure['timeOffset']
        departure_time = base_date + timedelta(minutes=time_offset)
        formatted_departure_time = departure_time.strftime("%Y-%m-%d %H:%M")
        
        # Platform information
        platform = departure.get('platform', '')
        
        # Create processed record
        processed_record = {
            'from_station': from_station,
            'from_station_id': from_station_id,
            'line_terminal': direction,
            'line_origin': departure['line']['origin'],
            'line_id': line_id,
            'line_name': line_name,
            'line_info': line_info,
            'direction_id': direction_id,
            'departure_time': formatted_departure_time,
            'departure_datetime': departure_time,
            'platform': platform,
            'next_station': None,
            'arrival_time': None
        }
        
        processed_data.append(processed_record)
    
    print("Converting to pandas DataFrame...")
    # Convert to DataFrame for faster processing
    df = pd.DataFrame(processed_data)
    
    print("Sorting departures chronologically...")
    # Sort by departure time
    df_sorted = df.sort_values('departure_datetime')
    
    # Create a dictionary to store the sorted departures for each line/direction combination
    print("Creating lookup structures...")
    line_direction_groups = {}
    for _, row in tqdm(df_sorted.iterrows(), desc="Creating lookup", total=len(df_sorted)):
        key = (row['line_id'], row['line_terminal'], row['line_origin'], row['direction_id'])
        if key not in line_direction_groups:
            line_direction_groups[key] = []
        line_direction_groups[key].append((row['departure_datetime'], row['from_station'], row['departure_time']))
    
    # Function to find next station for a departure
    def find_next_station(row):
        key = (row['line_id'], row['line_terminal'], row['line_origin'], row['direction_id'])
        departure_time = row['departure_datetime']
        
        if key in line_direction_groups:
            same_line_departures = line_direction_groups[key]
            # Filter departures that are after the current one
            next_departures = [(dt, station, dep_time) for dt, station, dep_time in same_line_departures if dt > departure_time]
            
            if next_departures:
                # Sort by time to get the earliest departure
                next_departures.sort()
                _, next_station, arrival_time = next_departures[0]
                return pd.Series([next_station, arrival_time])
        
        return pd.Series([None, None])
    
    print("Finding next stations and calculating arrival times (in parallel)...")
    # Apply the function in parallel to find next stations and arrival times
    result = df.p_apply(
        find_next_station, 
        axis=1,
    )
    
    # Update the DataFrame with the results
    df[['next_station', 'arrival_time']] = result
    
    print("Cleaning up temporary data...")
    # Clean up temporary fields
    df = df.drop('departure_datetime', axis=1)
    
    # Convert back to list of dictionaries
    processed_data = df.to_dict('records')
    
    print(f"Processing complete. Processed {len(processed_data)} departures.")
    return processed_data

def stationdf2rows(df):
    """
    Transform a stations DataFrame to a format suitable for Neo4j import.
    Specifically handles coordinates in format {'x': longitude, 'y': latitude}
    """
    rows = []
    for index, row in df.iterrows():
        # Extract station data
        try:
            aliases = row.aliasses if pd.notna(row.aliasses).all() else []
        except (AttributeError, ValueError):
            aliases = []
            
        station_data = {
            "geofoxid": row.id,  # Assuming 'id' is the field with "Master:xxxxx"
            "name": row['name'],
            "city": row.city if hasattr(row, 'city') else None,
            "vehicleTypes": row.vehicleTypes if hasattr(row, 'vehicleTypes') else [],
            "aliasses": aliases
        }
        
        # Handle coordinate conversion
        if hasattr(row, 'coordinate') and pd.notna(row.coordinate):
            try:
                # If it's already a dictionary
                if isinstance(row.coordinate, dict):
                    station_data["longitude"] = row.coordinate.get('x')
                    station_data["latitude"] = row.coordinate.get('y')
                # If it's a string representation of a dictionary
                elif isinstance(row.coordinate, str):
                    import ast
                    coord_dict = ast.literal_eval(row.coordinate)
                    station_data["longitude"] = coord_dict.get('x')
                    station_data["latitude"] = coord_dict.get('y')
                else:
                    station_data["longitude"] = None
                    station_data["latitude"] = None
            except Exception as e:
                print(f"Error processing coordinates for row {index}: {e}")
                station_data["longitude"] = None
                station_data["latitude"] = None
        else:
            station_data["longitude"] = None
            station_data["latitude"] = None
        
        rows.append(station_data)
    
    return rows