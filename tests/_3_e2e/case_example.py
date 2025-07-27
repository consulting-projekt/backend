import pandas as pd


test_cases = [
    {
        "vars": {
            "anfrage": "Ich möchte in 3 Stunden bei der Statue Bismarck sein",
            # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "start": "Hauptbahnhof",
            "answer": "Die nächste Verbindung <TRANSPORT> <LINE> mit Fahrrichtung <DIRECTION> startet von <START> um <TIME>. Möchtest du noch etwas wissen?"
            #'answer': "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST> um <TIME>." 
            #"answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen dir eine angenehme Fahrt!"
        }
    }
]


def generate_tests():
    return test_cases
