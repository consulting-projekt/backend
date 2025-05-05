import pandas as pd


test_cases = [
    {
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": None,  # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "date": None,  # hiermit kann simuliert werden dass systemseitig aktueller Tag verwendet wird
            "time": None,  # hiermit kann simuliert werden dass systemseitig aktuelle Zeit verwendet wird
            "answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen Ihnen eine angenehme Fahrt!"
        }
    },
    {
        "vars": {
            "anfrage": "Ich brauche nächste Woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": None,
            "date": None,
            "time": None,
            "answer": "Am <DATE> fährt ein Bus von der Station <START> zur Station <DEST>. Die Abfahrt ist um <TIME>. Wir wünschen Ihnen eine gute Reise!"
        }
    },
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?",
            "start": None,
            "date": None,
            "time": None,
            "answer": "Der nächste Bus fährt um <TIME> von der Station <START> zur Station <DEST>. Gute Fahrt!"
        }
    },
]


def generate_tests():
    return test_cases
