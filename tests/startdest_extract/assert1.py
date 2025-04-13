from typing import Dict, Any, Union
import json
from pythelpers.logger.logger import start_logging2
from pathlib import Path
import re

log_dir = Path(__file__).parent / "logs"


def get_assert(output: str, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    with start_logging2(logs_dirpath=log_dir):
        # test case variablen
        anfrage = options.get('vars', {}).get('anfrage', "")
        expected_output = options.get('vars', {}).get('assert', {})

        # llm output
        raw_llm_output = output

        # test start
        try:
            llm_json = raw_llm2json(raw_llm_output)
            if not llm_json:
                return False
                
            # Calculate score based on matching entries
            score = calculate_score(llm_json, expected_output)
            return score
                
        except Exception as e:
            print("Error:", e)
            return False


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
            
        # Check for required fields and verify they are lists
        required_fields = ["start", "start_typ", "ziel", "ziel_typ"]
        for field in required_fields:
            if field not in json_output:
                print(f"Error: Missing '{field}' field")
                return False
            if not isinstance(json_output[field], list):
                print(f"Error: Field '{field}' is not a list")
                return False
        
        # We'll print warnings but not fail validation if lengths don't match
        if len(json_output["start"]) != len(json_output["start_typ"]):
            print("Warning: 'start' and 'start_typ' lists have different lengths")
            
        if len(json_output["ziel"]) != len(json_output["ziel_typ"]):
            print("Warning: 'ziel' and 'ziel_typ' lists have different lengths")
            
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
    Still gives partial credit when lengths don't match but some elements are correct.
    """
    try:
        if not expected_json:
            print("Warning: No expected output provided for comparison")
            return 1.0  # Assume correct if no expected output is provided
        
        total_possible_matches = 0
        actual_matches = 0
        
        # Compare start entities
        if "start" in expected_json and len(expected_json["start"]) > 0:
            expected_starts = set(expected_json["start"])
            llm_starts = set(llm_json["start"])
            
            # Count matches for start entities
            start_matches = len(expected_starts.intersection(llm_starts))
            total_in_expected = len(expected_starts)
            total_in_llm = len(llm_starts)
            
            # Add to our running totals
            actual_matches += start_matches
            total_possible_matches += max(total_in_expected, total_in_llm)
            
            print(f"Start entities: {start_matches}/{max(total_in_expected, total_in_llm)} matches")
        
        # Compare start_typ
        if "start_typ" in expected_json and len(expected_json["start_typ"]) > 0:
            expected_start_types = set(expected_json["start_typ"])
            llm_start_types = set(llm_json["start_typ"])
            
            # Count matches for start types
            start_type_matches = len(expected_start_types.intersection(llm_start_types))
            total_in_expected = len(expected_start_types)
            total_in_llm = len(llm_start_types)
            
            # Add to our running totals
            actual_matches += start_type_matches
            total_possible_matches += max(total_in_expected, total_in_llm)
            
            print(f"Start types: {start_type_matches}/{max(total_in_expected, total_in_llm)} matches")
        
        # Compare ziel entities
        if "ziel" in expected_json and len(expected_json["ziel"]) > 0:
            expected_ziels = set(expected_json["ziel"])
            llm_ziels = set(llm_json["ziel"])
            
            # Count matches for ziel entities
            ziel_matches = len(expected_ziels.intersection(llm_ziels))
            total_in_expected = len(expected_ziels)
            total_in_llm = len(llm_ziels)
            
            # Add to our running totals
            actual_matches += ziel_matches
            total_possible_matches += max(total_in_expected, total_in_llm)
            
            print(f"Ziel entities: {ziel_matches}/{max(total_in_expected, total_in_llm)} matches")
        
        # Compare ziel_typ
        if "ziel_typ" in expected_json and len(expected_json["ziel_typ"]) > 0:
            expected_ziel_types = set(expected_json["ziel_typ"])
            llm_ziel_types = set(llm_json["ziel_typ"])
            
            # Count matches for ziel types
            ziel_type_matches = len(expected_ziel_types.intersection(llm_ziel_types))
            total_in_expected = len(expected_ziel_types)
            total_in_llm = len(llm_ziel_types)
            
            # Add to our running totals
            actual_matches += ziel_type_matches
            total_possible_matches += max(total_in_expected, total_in_llm)
            
            print(f"Ziel types: {ziel_type_matches}/{max(total_in_expected, total_in_llm)} matches")
        
        # Calculate final score
        if total_possible_matches == 0:
            return 1.0  # Avoid division by zero
        
        score = actual_matches / total_possible_matches
        print(f"Final score: {score:.2f} ({actual_matches}/{total_possible_matches})")
        return score
        
    except Exception as e:
        print(f"Error calculating score: {e}")
        return 0.0


if __name__ == "__main__":
    # Example usage
    output = """
```json
{
    "start": ["Innenstadt"],
    "start_typ": ["poi_or_aoi"],
    "ziel": [],
    "ziel_typ": []
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