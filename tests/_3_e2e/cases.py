import pandas as pd


test_cases = [
    {
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": None,  # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "date": None,  # hiermit kann simuliert werden dass systemseitig aktueller Tag verwendet wird
            "time": None,  # hiermit kann simuliert werden dass systemseitig aktuelle Zeit verwendet wird
            "answer": """Beispiel antwort"""
        }
    },
    {
        "vars": {
            "anfrage": "Ich brauche nächste woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": None,
            "date": None,
            "time": None,
            "answer": """Beispiel antwort"""
        }
    },
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?",
            "start": None,
            "date": None,
            "time": None,
            "answer": """Beispiel antwort"""
        }
    },
]


def generate_tests():
    return test_cases
