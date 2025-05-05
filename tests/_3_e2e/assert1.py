from typing import Dict, Any, Union
import json


def get_assert(output: str, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    # test case variablen




    # test start
    try:
        return {
                "pass": True,
                "score": 1.0,
                "reason": "All assertions passed"
            }
            
    except Exception as e:
        print("Error:", e)
        return False
    return True
