import pandas as pd


test_cases = [
    {
        "vars": {
            "anfrage": "Ich brauche um ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "start": None,
            'answer': "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>." 
            #"answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen dir eine angenehme Fahrt!"
        }
    },
    {
        "vars": {
            "anfrage": "Ich brauche nächste Woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": "Harverdstraße",
            "answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
        }
    },
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?",
            "start": None,
            "answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
        }
    },
]


def generate_tests():
    return test_cases
