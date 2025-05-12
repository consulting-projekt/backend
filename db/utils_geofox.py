import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
from parallel_pandas import ParallelPandas
from dateutil import relativedelta

# Initialize parallel pandas
ParallelPandas.initialize(n_cpu=12, disable_pr_bar=False)

file_dir = Path(__file__).resolve(strict=True).parent
data_dir = file_dir / "data_geofox"
data_departures_dir = data_dir / "departures"
service_types = ['ZUG', 'BUS']


def get_stations(client, loadFromDisk=False, doSave=True):
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


def get_departures(client, stations, filename="departures.json", loadFromDisk=False, doSave=True):
    if loadFromDisk:
        # load json from folder "data_geofox"
        with open(os.path.join(data_departures_dir, filename), "r") as f:
            res = json.load(f)
        return res

    # time 	GTITime Zeitpunkt, ab dem Abfahrten gesucht werden -> 03.04.2025 00:00:00
    time = {"date": "03.04.2025", "time": "00:00"}

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


def get_route_params1(date_str, time_str):
    time_param = {
        "date": get_date_param(date_str),
        "time": get_time_param(time_str)
    }

    return time_param


def get_route_params2(start, dest, time_is_departure, transport_type):
    """
    Transform Neo4j start/destination objects and extracted parameters into format
    needed for the get_route function.

    Args:
        start (dict): Neo4j start location object with location data
        dest (dict): Neo4j destination location object with location data
        params_extracted (dict): Dictionary with extracted routing parameters

    Returns:
        tuple: (start_param, dest_param, time_param, penalties_param)
    """
    # Transform start location to the required format
    start_param = {
        "type": "COORDINATE",
        "coordinate": {
            "x": start["location"]["lon"],
            "y": start["location"]["lat"]
        }
    }

    # Transform destination location to the required format
    dest_param = {
        "type": "COORDINATE",
        "coordinate": {
            "x": dest["location"]["lon"],
            "y": dest["location"]["lat"]
        }
    }

    # Handle penalties based on type of transport
    penalties_param = None

    if transport_type:
        penalties_param = [{
            "name": "DesiredType",
            "value": f"{transport_type}:-2"  # - 2 means Prefer
        }]

    return start_param, dest_param, penalties_param, time_is_departure


def get_date_param(date_str):
    current_date = datetime.now()

    # Parse date
    if date_str:
        if date_str == "today":
            target_date = current_date
            formatted_date = target_date.strftime("%d.%m.%Y")
        elif "today" in date_str:
            target_date = current_date
            # Check if it's addition or subtraction
            if "+" in date_str:
                parts = date_str.split("+")
                increments = parts[1].strip()
                target_date = apply_date_adjustments(target_date, increments)
            elif "-" in date_str:
                parts = date_str.split("-")
                decrements = parts[1].strip()
                target_date = apply_date_adjustments(
                    target_date, decrements, subtract=True)
            formatted_date = target_date.strftime("%d.%m.%Y")
        else:
            # Use the provided date directly if it's already well-formatted
            formatted_date = date_str
    else:
        formatted_date = current_date.strftime("%d.%m.%Y")

    return formatted_date


def apply_date_adjustments(base_date, adjustments, subtract=False):
    """
    Applies date adjustments (e.g., '3m3w5d') to the base_date.
    :param base_date: The starting datetime object.
    :param adjustments: A string containing adjustments like '3m3w5d'.
    :param subtract: Whether to subtract the adjustments instead of adding them.
    :return: Adjusted datetime object.
    """
    # Initialize adjustment values
    months, weeks, days = 0, 0, 0

    # Extract adjustments using simple parsing
    if "m" in adjustments:
        months = int(adjustments.split("m")[0])
        adjustments = adjustments.split("m")[1]
    if "w" in adjustments:
        weeks = int(adjustments.split("w")[0])
        adjustments = adjustments.split("w")[1]
    if "d" in adjustments:
        days = int(adjustments.split("d")[0])

    # Apply adjustments
    if subtract:
        adjusted_date = base_date - relativedelta(months=months)
        adjusted_date -= timedelta(weeks=weeks, days=days)
    else:
        adjusted_date = base_date + relativedelta(months=months)
        adjusted_date += timedelta(weeks=weeks, days=days)

    return adjusted_date


def get_time_param(time_str):
    current_date = datetime.now()

    # Parse time
    if time_str:
        if time_str == "now":
            formatted_time = current_date.strftime("%H:%M")
        elif "now" in time_str:
            target_time = current_date
            # Check if it's addition or subtraction
            if "+" in time_str:
                parts = time_str.split("+")
                increments = parts[1].strip()
                # Parse multiple increments like "2h35m"
                hours, minutes = 0, 0
                if "h" in increments:
                    hours = int(increments.split("h")[0])
                    increments = increments.split("h")[1]
                if "m" in increments:
                    minutes = int(increments.split("m")[0])
                target_time += timedelta(hours=hours, minutes=minutes)
            elif "-" in time_str:
                parts = time_str.split("-")
                decrements = parts[1].strip()
                # Parse multiple decrements like "2h35m"
                hours, minutes = 0, 0
                if "h" in decrements:
                    hours = int(decrements.split("h")[0])
                    decrements = decrements.split("h")[1]
                if "m" in decrements:
                    minutes = int(decrements.split("m")[0])
                target_time -= timedelta(hours=hours, minutes=minutes)
            formatted_time = target_time.strftime("%H:%M")
        else:
            # Use the provided time directly
            formatted_time = time_str
    else:
        formatted_time = current_date.strftime("%H:%M")

    return formatted_time


def get_route(client, start, dest, time=None, penalties=None, timeIsDeparture=True):
    endpoint = 'getRoute'

    # Beispiel für Abfahrtszeit
    # wenn None wird aktuelle Zeit verwendet
    # time = {
    #         "date": "22.04.2025", "time": "18:30"
    #     }

    # beispiel für penalty
    # penalties = [{
    #     "name": "DesiredType", "value": "u:-10"
    # }]

    # start = { # Beh\u00f6rde f\u00fcr Stadtentwicklung und Wohnen
    #         "type": "COORDINATE",
    #         "coordinate": {
    #                 "x": 10.004187,
    #                 "y": 53.497465
    #             },
    #     }

    # dest = { # "Altonaer Segel-Club e.V."
    #         "type": "COORDINATE",
    #         "coordinate": {
    #                 "x": 9.858205,
    #                 "y": 53.537384
    #             },
    #     }

    request = {
        "language": "de",
        "version": 59,
        "tariffDetails": False,
        "start": start,
        "dest": dest,
        "time": time,   # Zeit im Format GTITime: abfahrtszeit wenn timeIsDeparture = True, ankunftszeit wenn timeIsDeparture = False
        "timeIsDeparture": timeIsDeparture,
        "penalties": penalties,
    }

    res = client.send(endpoint, request)
    if 'realtimeAffected' in res and res['realtimeAffected']:
        schedules = res['realtimeSchedules']
    else:
        schedules = res['schedules']

    return schedules


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
        key = (row['line_id'], row['line_terminal'],
               row['line_origin'], row['direction_id'])
        if key not in line_direction_groups:
            line_direction_groups[key] = []
        line_direction_groups[key].append(
            (row['departure_datetime'], row['from_station'], row['departure_time']))

    # Function to find next station for a departure
    def find_next_station(row):
        key = (row['line_id'], row['line_terminal'],
               row['line_origin'], row['direction_id'])
        departure_time = row['departure_datetime']

        if key in line_direction_groups:
            same_line_departures = line_direction_groups[key]
            # Filter departures that are after the current one
            next_departures = [(dt, station, dep_time) for dt, station,
                               dep_time in same_line_departures if dt > departure_time]

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


def get_pois(client, filename="pois.json", maxList=1, loadFromDisk=False, doSave=True):
    if loadFromDisk:
        # load json from folder "data_geofox"
        with open(os.path.join(data_dir, filename), "r") as f:
            res = json.load(f)
        return res

    sdName = {
        "type": "POI",
        "combinedName": "Hamburg",
    }

    endpoint = 'checkName'

    request = {
        "language": "de",
        "version": 59,
        "tariffDetails": True,
        "maxList": maxList,
        "theName": sdName,
    }

    res = client.send(endpoint, request)

    if doSave and not loadFromDisk:
        # saving json to folder "data_geofox"
        with open(os.path.join(data_dir, filename), "w") as f:
            json.dump(res, f, indent=4)

    return res


def poisdf2rows(df):
    """
    Transform a stations DataFrame to a format suitable for Neo4j import.
    Specifically handles coordinates in format {'x': longitude, 'y': latitude}
    """
    rows = []
    for index, row in df.iterrows():
        # Extract station data

        station_data = {
            "geofoxid": row.id,  # Assuming 'id' is the field with "Master:xxxxx"
            "name": row['name'],
            "city": row.city if hasattr(row, 'city') else None,
            "address": row['address']
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


def get_station_innercityinfo(client, filename="stations_inner_city.json", maxList=1, loadFromDisk=False, doSave=True):
    if client is None:
        # load json from folder "data_geofox"
        with open(os.path.join(data_dir, filename), "r") as f:
            res = json.load(f)
        return res

    sdName = {
        "type": "STATION",
        "combinedName": "Hamburg",
    }

    endpoint = 'checkName'
    request = {
        "language": "de",
        "version": 59,
        "tariffDetails": True,
        "maxList": maxList,
        "theName": sdName,
    }

    res = client.send(endpoint, request)

    if doSave and not loadFromDisk:
        # saving json to folder "data_geofox"
        with open(os.path.join(data_dir, filename), "w") as f:
            json.dump(res, f, indent=4)

    return res


def get_startdest(client, anfrage):
    '''
    Get start and destination from a Qdrant client.
    anfrage type: 
        {
            "start": str|None,
            "dest": str|None,
            "dest_aoi": str|None
        }

    return type: (start, dest)
    '''
    start = anfrage.get("start")
    dest, dest_cond = anfrage.get("dest"), anfrage.get("dest_aoi")

    start = get_point_byquery(client, start, None)
    dest = get_point_byquery(client, dest, dest_cond)

    return start, dest


def get_point_byquery(client, point, point_cond):
    coordinate = None
    if point_cond:
        res_cond = check_name(client, point_cond)
        coordinate = res_cond['coordinate'] if res_cond else None
    res = check_name(client, point, coordinate=coordinate)
    if res:
        res2 = {}
        res2['location'] = res['coordinate']
        res2['name'] = res['name']
        return res2
    return None


def check_name(client, search_str, coordinate=None,  maxList=5):
    if search_str is None:
        return None

    endpoint = 'checkName'

    sdName = {
        "type": "UNKNOWN",
        "name": search_str,
        "city": "Hamburg",
    }

    if coordinate:
        sdName['coordinate'] = coordinate

    request = {
        "language": "de",
        "version": 59,
        "tariffDetails": True,
        "maxList": maxList,
        "theName": sdName,
        "allowTypeSwitch": True
    }

    res = client.send(endpoint, request)

    if res['returnCode'] == 'OK':
        if res.get('results', None):
            # Extract the first result
            res = res['results'][0]
            return res
    else:
        print(
            f"Error: {res['returnCode']} - {res['errorDevInfo']}, anfrage: {sdName}")

    return None
