import pandas as pd

test_cases = [
                { 
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.", 
            "assert": {
                "start": None,
                "start_condition": None,
                "dest": "Innenstadt",
                "dest_condition": None,
                "date": "today", # wenn datum konkret angegeben dann ist das das Zielformat: "22.04.2025"
                "time": "15:00",  # wenn zeit konkret angegeben dann ist das das Zielformat: "18:30"
                "time_is_departure": True, # wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
                "type_of_transport": ["bus"] # mögliche Werte: ["bus", "train"]
            }
        }
    },
            { 
        "vars": {
            "anfrage": "Ich brauche nächste woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.", 
            "assert": {
                "start": "Harverdstraße",
                "start_condition": None,
                "dest": "Innenstadt",
                "dest_condition": None,
                "date": "today + 7d",
                "time": "now + 2h", 
                "time_is_departure": True,
                "type_of_transport": ["bus"]
            }
        }
    },
    { 
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
            "assert": {
                "start": None,
                "start_condition": None,
                "dest": "Innenstadt",
                "dest_condition": None,
                "date": "today", 
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": ["bus"]
            }
        }
    }, 
        { 
        "vars": {
            "anfrage": "Ich brauche in 2 Stunden einen Zug in die Innenstadt. Gib mir die Route dazu.", 
            "assert": {
                "start": None,
                "start_condition": None,
                "dest": "Innenstadt",
                "dest_condition": None,
                "date": "today",
                "time": "now + 2h",
                "time_is_departure": True,
                "type_of_transport": ["train"]  
            }
        }
    }, 
        { 
        "vars": {
            "anfrage": "Gib mir eine Verbindung in die Innenstadt. Die Ankunft soll 15:00 sein.", 
            "assert": {
                "start": None,
                "start_condition": None,
                "dest": "Innenstadt",
                "dest_condition": None,
                "date": "today", 
                "time": "15:00",
                "time_is_departure": False,
                "type_of_transport": None  
            }
        }
    }, 
]


def generate_tests():
    return test_cases