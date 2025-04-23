from typing import Dict, Any, Union
import json
from pythelpers.logger.logger import start_logging2
from pathlib import Path
import re

log_dir = Path(__file__).parent / "logs"


def get_assert(output: str, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    # test case variablen
    anfrage = options.get('vars', {}).get('anfrage', "")
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
            
        # Calculate score based on matching entries
        score = calculate_score(llm_json, expected_output)
        if score < 1.0:
            return {
                "pass": False,
                "score": score,
                "reason": f"Partial match with score {score}, expected 1.0"
            }
        else:
            return {
                "pass": True,
                "score": score,
                "reason": "Perfect match"
            }
            
    except Exception as e:
        print("Error:", e)
        return {
            "pass": False,
            "score": 0.0,
            "reason": e
        }


def raw_llm2json(raw_llm_output):
    try:
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
        required_fields = ["start", "start_aoi", "dest", "dest_aoi"]
        for field in required_fields:
            if field not in json_output:
                print(f"Error: Missing '{field}' field")
                return False
            # Check that each field is either null or a string
            if json_output[field] is not None and not isinstance(json_output[field], str):
                print(f"Error: Field '{field}' is not null or a string")
                return False
            
        return json_output
            
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    

def calculate_score(llm_json, expected_json):
    """
    Calculate a score based on matching entries in the LLM output compared to expected output.
    For the new schema where fields are single values instead of lists.
    """
    try:
        if not expected_json:
            print("Warning: No expected output provided for comparison")
            return 1.0  # Assume correct if no expected output is provided
        
        total_fields = 0
        matched_fields = 0
        
        # Fields to check
        fields_to_check = ["start", "start_aoi", "dest", "dest_aoi"]
        
        for field in fields_to_check:
            if field in expected_json and field in llm_json:
                total_fields += 1
                
                # Both are null/None - this is a match
                if expected_json[field] is None and llm_json[field] is None:
                    matched_fields += 1
                    print(f"{field}: Match - Both are null")
                
                # Both have values - check if they match
                elif expected_json[field] is not None and llm_json[field] is not None:
                    if expected_json[field].lower() == llm_json[field].lower():
                        matched_fields += 1
                        print(f"{field}: Match - '{expected_json[field]}'")
                    else:
                        print(f"{field}: Mismatch - Expected '{expected_json[field]}', got '{llm_json[field]}'")
                
                # One is null, one has value - this is a mismatch
                else:
                    expected_value = "null" if expected_json[field] is None else f"'{expected_json[field]}'"
                    llm_value = "null" if llm_json[field] is None else f"'{llm_json[field]}'"
                    print(f"{field}: Mismatch - Expected {expected_value}, got {llm_value}")
        
        # Calculate final score
        if total_fields == 0:
            return 1.0  # Avoid division by zero
        
        score = matched_fields / total_fields
        print(f"Final score: {score:.2f} ({matched_fields}/{total_fields})")
        return score
        
    except Exception as e:
        print(f"Error calculating score: {e}")
        return 0.0



if __name__ == "__main__":
    # Example usage
    output = """
```json
{
    "start": ["Herthastraße"],
    "start_typ": ["poi_or_aoi"],
    "dest": ["Innenstadt"],
    "ziel_typ": ["poi_or_aoi"]
}
```"""
    options = {
        'vars': {
            'anfrage': 'Zeige mir eine Verbindung von Herthastraße zur Innenstadt?',
            'assert': {
                'start': ['Herthastraße'],
                'start_typ': ['adress'],
                'ziel': ['Innenstadt'],
                'ziel_typ': ['poi_or_aoi']
            }
        }
    }
    
    score = get_assert(output, options)
    print("Score:", score)