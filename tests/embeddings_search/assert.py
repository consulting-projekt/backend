from typing import Dict, Any, Union
import json
from pythelpers.logger.logger import start_logging2
from pathlib import Path
import re

log_dir = Path(__file__).parent / "logs"

import re
import json
import math
from typing import Dict, Any, Union



def get_assert(output, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    # test case variables
    expected_output = options.get('vars', {}).get('assert', {})

    # llm output
    raw_llm_output = output

    # test start
    try:
        llm_json = raw_llm2json(raw_llm_output)
        if not llm_json:
            return {
                "pass": False,
                "score": 0.0,
                "reason": "Invalid JSON format or structure"
            }
            
        # Check all the expected assertions
        results = check_all_assertions(llm_json, expected_output)
        
        if results["pass"]:
            return {
                "pass": True,
                "score": results["score"],
                "reason": "All assertions passed"
            }
        else:
            return {
                "pass": False,
                "score": results["score"],
                "reason": results["reason"]
            }
            
    except Exception as e:
        print("Error:", e)
        return {
            "pass": False,
            "score": 0.0,
            "reason": str(e)
        }


def raw_llm2json(raw_llm_output):
    try:
        # If output is already a dict or similar structure
        if isinstance(raw_llm_output, (dict, list, tuple)):
            if isinstance(raw_llm_output, tuple) and len(raw_llm_output) == 1:
                # Handle tuple with single dict
                json_output = raw_llm_output[0]
            else:
                json_output = raw_llm_output
        else:
            # Check if the text contains markdown code block
            json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            matches = re.findall(json_pattern, raw_llm_output)
            
            if matches:
                # Use the first JSON code block found
                json_str = matches[0].strip()
                json_output = json.loads(json_str)
            else:
                # Try parsing the entire text as JSON
                json_output = json.loads(raw_llm_output)
        
        # Check if it has the expected structure
        if not isinstance(json_output, dict):
            print("Error: Output is not a dictionary")
            return False
            
        # Check for required fields
        required_fields = ["start", "dest"]
        for field in required_fields:
            if field not in json_output:
                print(f"Error: Missing '{field}' field")
                return False
        
        # The output should have start and dest fields (both can be None or dictionaries)
        # We don't need to convert to lists as they are single entities
        
        # If dest is present but ziel isn't, map dest to ziel
        if "dest" in json_output and "ziel" not in json_output:
            json_output["ziel"] = json_output["dest"]
        
        return json_output
            
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def check_all_assertions(llm_json, expected_json):
    """
    Check all the assertions in the expected_json against the llm_json output
    Returns a dict with pass status, score, and reason
    """
    if not expected_json:
        return {"pass": True, "score": 1.0, "reason": "No assertions to check"}
    
    # Track all assertion results
    all_passed = True
    reasons = []
    total_assertions = 0
    passed_assertions = 0
    
    # Check start assertions if any
    if "start_name_contains" in expected_json and llm_json.get("start"):
        total_assertions += 1
        if check_name_contains(llm_json["start"], expected_json["start_name_contains"]):
            passed_assertions += 1
        else:
            all_passed = False
            reasons.append("start_name_contains assertion failed")
    
    # Check ziel/dest name assertions
    if "ziel_name_contains" in expected_json and llm_json.get("ziel"):
        total_assertions += 1
        if check_name_contains(llm_json["ziel"], expected_json["ziel_name_contains"]):
            passed_assertions += 1
        else:
            all_passed = False
            reasons.append(f"ziel_name_contains assertion failed, {llm_json['ziel']} does not contain {expected_json['ziel_name_contains']}")
    
    # Check ziel/dest location assertions
    if "ziel_nahe" in expected_json and llm_json.get("ziel"):
        total_assertions += 1
        
        # Extract the point and radius (if provided)
        if isinstance(expected_json["ziel_nahe"], list):
            point_str = expected_json["ziel_nahe"][0]
            radius_meters = expected_json["ziel_nahe"][1]
        else:
            point_str = expected_json["ziel_nahe"]
            radius_meters = 1000  # Default to 1km if not specified
            
        is_near, distance = check_location_near(llm_json["ziel"], point_str, radius_meters)
        if is_near:
            passed_assertions += 1
        else:
            all_passed = False
            reasons.append(f"ziel_nahe assertion failed - not within {radius_meters}m of {point_str}, distance: {distance:.2f}m")
    
    # Calculate score
    score = passed_assertions / max(total_assertions, 1)
    
    return {
        "pass": all_passed,
        "score": score,
        "reason": "; ".join(reasons) if reasons else "All assertions passed"
    }


def check_name_contains(entity, name_patterns):
    """
    Check if the entity has a name that contains any of the patterns in name_patterns
    """
    if not entity:
        return False
        
    # Make sure name_patterns is a list
    if isinstance(name_patterns, str):
        name_patterns = [name_patterns]
    
    # Extract name from entity
    if isinstance(entity, dict):
        entity_name = entity.get("name", "")
    else:
        entity_name = str(entity)
        
    # Convert to lowercase for case-insensitive matching
    entity_name_lower = entity_name.lower()
    
    # Check if any pattern is in the entity name
    for pattern in name_patterns:
        if pattern.lower() in entity_name_lower:
            return True
    
    return False


def check_location_near(entity, point_str, max_distance_meters):
    """
    Check if the entity's location is within max_distance_meters of point_str
    point_str format: "POINT(longitude latitude)"
    """
    if not entity:
        return False
    
    # Extract coordinates from the point string
    match = re.match(r"POINT\(([0-9.-]+)\s+([0-9.-]+)\)", point_str)
    if not match:
        print(f"Invalid point format: {point_str}")
        return False
    
    reference_lon = float(match.group(1))
    reference_lat = float(match.group(2))
    
    # Extract location from entity
    if not isinstance(entity, dict):
        return False
    
    location = entity.get("location")
    if not location:
        return False
        
    # Handle different location formats
    if isinstance(location, list) and len(location) >= 2:
        entity_lon, entity_lat = location[0], location[1]
    elif isinstance(location, dict) and "lon" in location and "lat" in location:
        entity_lon, entity_lat = location["lon"], location["lat"]
    elif isinstance(location, dict) and "longitude" in location and "latitude" in location:
        entity_lon, entity_lat = location["longitude"], location["latitude"]
    else:
        return False
        
    # Calculate distance
    distance_meters = calculate_distance(
        reference_lat, reference_lon, 
        entity_lat, entity_lon
    )
    
    # Check if distance is within the maximum
    return distance_meters <= max_distance_meters, distance_meters


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth specified by latitude/longitude
    using the Haversine formula. Returns distance in meters.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371000  # Earth radius in meters
    
    return c * r


def calculate_score(llm_json, expected_json):
    """
    Calculate a score based on matching entries in the LLM output compared to expected output.
    Now supports the new assertion types.
    """
    # Use the comprehensive check_all_assertions function
    result = check_all_assertions(llm_json, expected_json)
    return result["score"]



if __name__ == "__main__":
    # Example usage
    output =  {
            "start": None,
            "dest": {
                    'neo4j_elementId': '4:30f9f47a-615f-4018-a291-0f284d9f1880:11600', 
                    'name': 'Evangelisch-reformierte Kirche', 
                    'description': '', 
                    'tags': [], 
                    'label': 'POI', 
                    'location': [10.000413, 53.554069], 
                    'score': 0.71740854
                }
        },
    options = {
        'vars': {
            'anfrage': {
            "start": None,
            "start_bedingung": None,
            "ziel": "Kirche",
            "ziel_bedingung": "Kirchdorf-Süd"
            },
            'assert': {
                "ziel_nahe": ["POINT(10.000413 53.554069)", 2000]
            }
        }
    }
    
    score = get_assert(output, options)
    print("Score:", score)