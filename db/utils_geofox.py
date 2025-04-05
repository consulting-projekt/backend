from geofox_client import GtiClient
import json
import os
from pathlib import Path
import pandas as pd


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

    if doSave:
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

    if doSave:
        # saving json to folder "data_geofox"
        with open(os.path.join(data_departures_dir, filename), "w") as f:
            json.dump(res, f, indent=4)

    return res


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
            "name": row.name,
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