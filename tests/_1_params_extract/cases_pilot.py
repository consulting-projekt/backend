import pandas as pd

test_cases = [
    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstatt?",
            "assert": {
                "start": None,

                "dest": "Innenstatt",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
]


def generate_tests():
    return test_cases
