import pandas as pd


test_cases = [
                { 
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.", 

                "start": None, # mögliche Werte: None, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
                "start_aoi": None, # mögliche Werte: None, <start aoi> wenn für "start" adresse|station|poi angegeben
                "dest": "Innenstadt", # mögliche Werte: <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
                "dest_aoi": None, # mögliche Werte: None, <dest aoi> wenn für "dest" adresse|station|poi angegeben
                "date": "today", # mögliche Werte: None, today, today + d|w (d:Tage, w:Wochen) Datum mit Zielformat: 22.04.2025
                "time": "15:00", # mögliche Werte: None, now, now + m|h (m:Minuten, h:Stunden) Zeit mit Zielformat: 18:30
                "time_is_departure": True, # mögliche Werte: True, False; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
                "type_of_transport": "bus" # mögliche Werte: None, bus, train
            
        }
    },
        { 
    "vars": {
        "anfrage": "Ich brauche nächste woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.", 

            "start": "Harverdstraße",
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today + 7d",
            "time": "now + 2h", 
            "time_is_departure": True,
            "type_of_transport": "bus"
        
    }
},
{ 
    "vars": {
        "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 

            "start": "Lutterothstraße",
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"
        
    }
}, 
    { 
    "vars": {
        "anfrage": "Ich brauche in 2 Stunden einen Zug in die Innenstadt. Gib mir die Route dazu.", 

            "start": None,
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today",
            "time": "now + 2h",
            "time_is_departure": True,
            "type_of_transport": "train"  
        
    }
}, 
    { 
    "vars": {
        "anfrage": "Gib mir eine Verbindung in die Innenstadt. Die Ankunft soll 15:00 sein.", 

            "start": None,
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today", 
            "time": "15:00",
            "time_is_departure": False,
            "type_of_transport": None  
        
    }
}, 
]


def generate_tests():
    return test_cases