import pandas as pd

# start und dest types = ["adress", "poi_or_aoi",  "station" , None]
test_cases = [
    { 
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
            "assert": {
                "start": [],
                "start_typ": [],
                "ziel": ["Innenstadt"],
                "ziel_typ": ["poi_or_aoi"]
            }
        }
    }, 
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zu einem Restarurant in Nähe vom Hafen?", 
            "assert": {
                "start": ["Herthastraße"],
                "start_typ": ["adress"],
                "ziel": ["Restarurant", "Hafen"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zur Innenstadt?", 
            "assert": {
                "start": ["Herthastraße"],
                "start_typ": ["adress"],
                "ziel": ["Innenstadt"],
                "ziel_typ": ["poi_or_aoi"]
            }
        }
    },
]


def generate_tests():
    return test_cases