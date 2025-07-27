from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402
from typing import Dict, Any, Union
import json
from pathlib import Path
import re
from src.utils_llm import raw_llm2json

log_dir = Path(__file__).parent / "logs"


def get_assert(output: str, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    # test case variables
    anfrage = options.get('vars', {}).get('anfrage', "")
   #print(output)
    expected_output = options.get('vars', {}).get('assert', {})

    # llm output
    raw_llm_output = output

    # test start
    try:
        llm_json = raw_llm2json(raw_llm_output)
        #print(llm_json)
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
            "reason": str(e)
        }


def calculate_score(llm_json, expected_json):
    """
    Calculate a score based on matching entries in the LLM output compared to expected output.
    For the new schema with the updated fields for public transportation queries.
    """
    try:
        if not expected_json:
            print("Warning: No expected output provided for comparison")
            return 1.0  # Assume correct if no expected output is provided

        total_fields = 0
        matched_fields = 0

        # Fields to check based on the new prompt format
        fields_to_check = [
            "start", "dest", "dest_aoi",
            "date", "time", "time_is_departure", "type_of_transport"
        ]

        for field in fields_to_check:
            if field in expected_json and field in llm_json:
                total_fields += 1

                # Both are null/None - this is a match
                if expected_json[field] is None and llm_json[field] is None:
                    matched_fields += 1
                    print(f"{field}: Match - Both are null")

                # Both have values - check if they match
                elif expected_json[field] is not None and llm_json[field] is not None:
                    # For boolean values (time_is_departure)
                    if isinstance(expected_json[field], bool) and isinstance(llm_json[field], bool):
                        if expected_json[field] == llm_json[field]:
                            matched_fields += 1
                            print(f"{field}: Match - '{expected_json[field]}'")
                        else:
                            print(
                                f"{field}: Mismatch - Expected '{expected_json[field]}', got '{llm_json[field]}'")
                    # For string values
                    elif isinstance(expected_json[field], str) and isinstance(llm_json[field], str):
                        if expected_json[field].lower() == llm_json[field].lower():
                            matched_fields += 1
                            print(f"{field}: Match - '{expected_json[field]}'")
                        else:
                            print(
                                f"{field}: Mismatch - Expected '{expected_json[field]}', got '{llm_json[field]}'")
                    else:
                        print(
                            f"{field}: Type Mismatch - Expected type '{type(expected_json[field])}', got '{type(llm_json[field])}'")

                # One is null, one has value - this is a mismatch
                else:
                    expected_value = "null" if expected_json[
                        field] is None else f"'{expected_json[field]}'"
                    llm_value = "null" if llm_json[field] is None else f"'{llm_json[field]}'"
                    print(
                        f"{field}: Mismatch - Expected {expected_value}, got {llm_value}")

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
    # Example usage with the new format
   # output = """
#json
#{
#    "start": null,
#    "dest": "Innenstadt",
#    "dest_aoi": null,
#    "date": "today",
#    "time": "now + 1h",
#    "time_is_departure": true,
#    "type_of_transport": "bus"
#}
#```"""
    output = """ 
```
<think>
Okay, let's tackle this user query. The user is asking for the next bus from Harvertstraße to the Innenstadt next week. First, I need to extract the entities as per the rules provided.

Starting with "start": The user mentions "von der Harvertstraße", which translates to "from Harvertstraße". So "start" should be "Harvertstraße". 

Next, "dest": The user says "in die Innenstadt", which is "to the Innenstadt". So "dest" is "Innenstadt". 

Now, "dest_aoi": Since the destination is a POI (Innenstadt) without a specific place or street mentioned, according to the rules, "dest_aoi" should be null. 

For "date": The user says "next week", which is "today + 1w" as per the rules. 

Time: The user didn't mention a specific time, so it's "now". But wait, the user didn't specify a time, so "time" is "now". However, the user might be implying that they want the next bus, so maybe the time is "now" as the default. 

Time_is_departure: Since the user is starting from Harvertstraße and taking the bus, the time is for departure, so "time_is_departure" is true. 

Type_of_transport: The user mentioned "Bus", so "type_of_transport" is "bus".

Let me check the rules again. The date is "next week" which is "today + 1w". The time is "now" because there's no specific time given. The start is Harvertstraße, dest is Innenstadt, and dest_aoi is null. 

I think that's all. Let me structure the JSON accordingly.
</think>

{
    "start": "Harvertstraße",
    "dest": "Innenstadt",
    "dest_aoi": null,
    "date": "today + 1w",
    "time": "now",
    "time_is_departure": true,
    "type_of_transport": "bus"
}
```"""

    options = {
        'vars': {
            'anfrage': 'Wann kommt der nächste Bus von Herthastraße in die Innenstadt?',
            'assert': {
                "start": None,  # mögliche Werte: None, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
                # mögliche Werte: None, <start aoi> wenn für "start" adresse|station|poi angegeben
                # mögliche Werte: None, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
                "dest": "Innenstadt",
                # mögliche Werte: None, <dest aoi> wenn für "dest" adresse|station|poi angegeben
                "dest_aoi": None,
                # mögliche Werte: None, today, today + d|w (d:Tage, w:Wochen) Datum mit Zielformat: 22.04.2025
                "date": "today",
                # mögliche Werte: None, now, now + m|h (m:Minuten, h:Stunden) Zeit mit Zielformat: 18:30
                "time": "15:00",
                # mögliche Werte: True, False; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
                "time_is_departure": True,
                "type_of_transport": "bus"  # mögliche Werte: None, bus, train
            }
        }
    }

    score = get_assert(output, options)
    print("Score:", score)
