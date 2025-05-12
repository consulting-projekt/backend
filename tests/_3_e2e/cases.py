import pandas as pd


test_cases = [
    {
        "vars": {
            "anfrage": "Ich brauche um ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "start": "Harverdstraße",
            "answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen dir eine angenehme Fahrt!"
        }
    },
    {
        "vars": {
            "anfrage": "Ich brauche nächste Woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": None,
            "answer": "Am <DATE> fährt ein Bus von der Station <START> zur Station <DEST>. Die Abfahrt ist um <TIME>. Wir wünschen dir eine gute Reise!"
        }
    },
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?",
            "start": None,
            "answer": "Sag uns bitte, von wo du starten möchtest? Sobald wir die Startstation kennen, können wir dir die nächste Verbindung nennen."
        }
    },
]


def generate_tests():
    return test_cases
