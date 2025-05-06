import pandas as pd


test_cases = [
    {
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "start": "Harverdstraße",
            "answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen Ihnen eine angenehme Fahrt!"
        }
    },
    {
        "vars": {
            "anfrage": "Ich brauche nächste Woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": None,
            "answer": "Am <DATE> fährt ein Bus von der Station <START> zur Station <DEST>. Die Abfahrt ist um <TIME>. Wir wünschen Ihnen eine gute Reise!"
        }
    },
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?",
            "start": None,
            "answer": "Könnten Sie uns bitte mitteilen, von wo Sie starten möchten? Sobald wir die Startstation kennen, können wir Ihnen die nächste Verbindung nennen."
        }
    },
]


def generate_tests():
    return test_cases
