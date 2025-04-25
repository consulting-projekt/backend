import pandas as pd


test_cases = [
    { 
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "response": "Der nächste Bus in die Innenstadt fährt um 15:23 Uhr ab.",
        }
    },
]


def generate_tests():
    return test_cases