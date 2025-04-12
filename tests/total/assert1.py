from typing import Dict, Any, Union
import json


def get_assert(output: str, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    # test case variablen
    anfrage = options.get('vars', {}).get('anfrage', "")
    user_location = options.get('vars', {}).get('user_location', "")

    # llm output
    raw_llm_output = output

    # test start
    try:
        json_output = raw_llm2json(raw_llm_output)
        if not json_output:
            return False
            
    except Exception as e:
        print("Error:", e)
        return False
    return True


def raw_llm2json(raw_llm_output):
        # Parse the JSON response from the llm
        json_output = json.loads(raw_llm_output)
        
        # Check if it has the expected structure
        if not isinstance(json_output, dict):
            print("Error: Output is not a dictionary")
            return False
            
        if "answer" not in json_output or not isinstance(json_output["answer"], str):
            print("Error: Missing or invalid 'answer' field")
            return False
            
        if "routes" not in json_output or not isinstance(json_output["routes"], list):
            print("Error: Missing or invalid 'routes' field")
            return False
            
        # Check each route has the required fields
        for route in json_output["routes"]:
            if not isinstance(route, dict):
                print("Error: Route is not a dictionary")
                return False
                
            if "start" not in route or not isinstance(route["start"], str):
                print("Error: Missing or invalid 'start' field in route")
                return False
                
            if "end" not in route or not isinstance(route["end"], str):
                print("Error: Missing or invalid 'end' field in route")
                return False
                
            if "duration" not in route or not isinstance(route["duration"], (int, float)):
                print("Error: Missing or invalid 'duration' field in route")
                return False
            
        return json_output
