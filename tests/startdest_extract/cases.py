import pandas as pd


test_cases = [
        { 
        "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
        "user_location": {"lat": 52.5200, "lon": 13.4050},
        "start_location": None,
        "assert": {
            "start": None,
            "dest": "Innenstadt"
        }
    }, 
]


def generate_tests():
    return test_cases