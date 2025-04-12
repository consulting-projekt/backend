import pandas as pd

# start und dest types = ["poi",  "adress", "aoi",  "station" , None]
test_cases = [
    { 
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
            "assert": {
                "start": ["leer"],
                "start_typ": None,
                "ziel": ["Innenstadt"],
                "ziel_type": "aoi"
            }
        }
    }, 
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zu einem Restarurant in Nähe vom Hafen?", 
            "assert": {
                "start": "Herthastraße",
                "start_typ": "adress",
                "ziel": "Restarurant in Nähe vom Hafen",
                "ziel_typ": "poi_complex"
            }
        }
    },
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zur Innenstadt?", 
            "assert": {
                "start": "Herthastraße",
                "start_typ": "adress",
                "ziel": "Innenstadt",
                "ziel_typ": "aoi"
            }
        }
    },
]


def generate_tests():
    return test_cases