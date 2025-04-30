import pandas as pd

test_cases = [
    { 
    "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.", 
            "assert": {
                "start": None, # mögliche Werte: None, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
                "start_aoi": None, # mögliche Werte: None, <start aoi> wenn für "start" adresse|station|poi angegeben
                "dest": "Innenstadt", # mögliche Werte: None, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
                "dest_aoi": None, # mögliche Werte: None, <dest aoi> wenn für "dest" adresse|station|poi angegeben
                "date": "today", # mögliche Werte: None, today, today + d|w (d:Tage, w:Wochen) Datum mit Zielformat: 22.04.2025
                "time": "15:00", # mögliche Werte: None, now, now + m|h (m:Minuten, h:Stunden) Zeit mit Zielformat: 18:30
                "time_is_departure": True, # mögliche Werte: True, False; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
                "type_of_transport": "bus" # mögliche Werte: None, bus, train
            }
        }
    },
        { 
    "vars": {
        "anfrage": "Ich brauche nächste woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.", 
        "assert": {
            "start": "Harverdstraße",
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today + 1w",
            "time": "now", 
            "time_is_departure": True,
            "type_of_transport": "bus"
        }
    }
},
{ 
    "vars": {
        "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"
        }
    }
}, 
    { 
    "vars": {
        "anfrage": "Ich brauche in 2 Stunden einen Zug in die Innenstadt. Gib mir die Route dazu.", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today",
            "time": "now + 2h",
            "time_is_departure": True,
            "type_of_transport": "train"  
        }
    }
}, 
    { 
    "vars": {
        "anfrage": "Gib mir eine Verbindung in die Innenstadt. Die Ankunft soll 15:00 sein.", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today", 
            "time": "15:00",
            "time_is_departure": False,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "LuftHansa Flughafen -> Rönkloppel in ca. 40 min", 
        "assert": {
            "start": "Flughafen",
            "start_aoi": None,
            "dest": "Rönkloppel",
            "dest_aoi": None,
            "date": "today", 
            "time": "now + 40m",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "in 30 min, Von der Alsterblick zum Höpengrund, mit dem zug", 
        "assert": {
            "start": "Alsterblick",
            "start_aoi": None,
            "dest": "Höpengrund",
            "dest_aoi": None,
            "date": "today", 
            "time": "now + 30m",
            "time_is_departure": True,
            "type_of_transport": "train"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Zug oder Bus egal, ich muss vom Kanzlershofer Weg zum Seehof", 
        "assert": {
            "start": "Kanzlershofer Weg",
            "start_aoi": None,
            "dest": "Seehof",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None 
        }
    }
},
{ 
    "vars": {
        "anfrage": "Morgen um 14 Uhr mi Zug, Graf-Otto-Weg : Pommernweg", 
        "assert": {
            "start": "Graf-Otto-Weg",
            "start_aoi": None,
            "dest": "Pommernweg",
            "dest_aoi": None,
            "date": "today + 1", 
            "time": "14:00",
            "time_is_departure": True,
            "type_of_transport": "train" 
        }
    }
},
{ 
    "vars": {
        "anfrage": "Meine Eltern kommen morgen in die Stadt. Welcher Bus geht vom Gottschalkweg zur Rehkoppel, so ca. 16:30 heute", 
        "assert": {
            "start": "Gottschalkweg",
            "start_aoi": None,
            "dest": "Rehkoppel",
            "dest_aoi": None,
            "date": "today", 
            "time": "16:30",
            "time_is_departure": True,
            "type_of_transport": "bus" 
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich fahre jetzt in Urlaub. Ich brauche einen Bus in 3 Wochen und 5 Tagen um 23 Uhr vom Flughafen zum Prinzenweg", 
        "assert": {
            "start": "Flughafen",
            "start_aoi": None,
            "dest": "Prinzenweg",
            "dest_aoi": None,
            "date": "today + 3w5d", 
            "time": "23:00",
            "time_is_departure": True,
            "type_of_transport": "bus" 
        }
    }
},
{ 
    "vars": {
        "anfrage": "23.07.2025, um 17 Uhr, Manshardstrasse nach Hellmesbergerweg, Zug", 
        "assert": {
            "start": "Manshardstrasse",
            "start_aoi": None,
            "dest": "Hellmesbergerweg",
            "dest_aoi": None,
            "date": "23.07.2025", 
            "time": "17:00",
            "time_is_departure": True,
            "type_of_transport": "train" 
        }
    }
},
{ 
    "vars": {
        "anfrage": "Bus oder zug. Ich muss am 23.Dezember 2026 von der Saseler Straße zum Skaldenweg, 5 Uhr morgens", 
        "assert": {
            "start": "Saseler Straße",
            "start_aoi": None,
            "dest": "Skaldenweg",
            "dest_aoi": None,
            "date": "23.12.2026", 
            "time": "05:00",
            "time_is_departure": True,
            "type_of_transport": None 
        }
    }
},
{ 
    "vars": {
        "anfrage": "8 Uhr abends, Wildschwanbrook nach Immenbusch, Bus", 
        "assert": {
            "start": "Wildschwanbrook",
            "start_aoi": None,
            "dest": "Immenbusch",
            "dest_aoi": None,
            "date": "today", 
            "time": "20:00",
            "time_is_departure": True,
            "type_of_transport": "bus" 
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich muss morgen um 23 Uhr am Kressenweg sein.Fahre von Siloahweg los, mit dem Bus bitte", 
        "assert": {
            "start": "Kressenweg",
            "start_aoi": None,
            "dest": "Siloahweg",
            "dest_aoi": None,
            "date": "today + 1d", 
            "time": "23:00",
            "time_is_departure": False,
            "type_of_transport": "bus" 
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich benötge die nächste Bus-Linie vom Hochrad zur Großen Brunnenstraße", 
        "assert": {
            "start": "Hochrad",
            "start_aoi": None,
            "dest": "Große Brunnenstraße",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Zeig mir bitte den nächsten Bus von der Station Meßberg zum Hauptbahnhof", 
        "assert": {
            "start": "Meßberg",
            "start_aoi": None,
            "dest": "Hauptbahnhof",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Muss Morgen um 2 Uhr Nachmittags am Eppendorfer Marktplatz sein, Von: Lauenstreinstraße, nur Bus, keine Züge", 
        "assert": {
            "start": "Lauenstreinstraße",
            "start_aoi": None,
            "dest": "Eppendorfer Marktplatz",
            "dest_aoi": None,
            "date": "today + 1", 
            "time": "14:00",
            "time_is_departure": False,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Wann geht der Nächste Bus zur Station Reeperbahn?", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Reeperbahn",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Wann geht der nächste Bus der Linie 151 vom Zollamt Waltershof zum Inselpark", 
        "assert": {
            "start": "Zollamt Waltershof",
            "start_aoi": None,
            "dest": "Inselpark",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Eidelstedter Platz nach Schubackstraße, jetzt", 
        "assert": {
            "start": "Eidelstedter Platz",
            "start_aoi": None,
            "dest": "Schubackstraße",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Wie komme ich jetzt von Luckmoor zum Habichtsplatz", 
        "assert": {
            "start": "Luckmoor",
            "start_aoi": None,
            "dest": "Habichtsplatz",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich brauche in 35 Minuten einen Bus vom Dörpsweg zur Richardstraße", 
        "assert": {
            "start": "Dörpsweg",
            "start_aoi": None,
            "dest": "Richardstraße",
            "dest_aoi": None,
            "date": "today", 
            "time": "now + 35m",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Wie komme ich von der Schnackenburgalle über die Bus Linie 172 zum Volkspark", 
        "assert": {
            "start": "Schnackenburgalle",
            "start_aoi": None,
            "dest": "Volkspark",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich muss zur Böttgerstraße", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Böttgerstraße",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Welche Bus-Linie fährt zwischen Suhrenkamp und Röntgenstraße", 
        "assert": {
            "start": "Suhrenkamp",
            "start_aoi": None,
            "dest": "Röntgenstraße",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich muss in 2h 35 min von Puckholm zum Rieck Museum. Wie komme ich dort hin?", 
        "assert": {
            "start": "Puckholm",
            "start_aoi": None,
            "dest": "Rieck Museum",
            "dest_aoi": None,
            "date": "today", 
            "time": "now + 2:35",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich muss zur Grundschule Kirchwerder und wieder zurück", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Grundschule Kirchwerder",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich benötige einen Bus der Linie 543 von der Eißendorfer Straße zum Vahrenwinkelweg. Anschließend benötige ich einen Bus vom Hainholzweg", 
        "assert": {
            "start": "Eißendorfer Straße",
            "start_aoi": None,
            "dest": "Vahrenwinkelweg",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich benötige einen Bus in 3 Stunden von der Eißendorfer Straße zum Vahrenwinkelweg", 
        "assert": {
            "start": "Eißendorfer Straße",
            "start_aoi": None,
            "dest": "Vahrenwinkelweg",
            "dest_aoi": None,
            "date": "today", 
            "time": "now + 3h",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich benötige einen Bus der Linie 543 von der Eißendorfer Straße zum Vahrenwinkelweg. Anschließend benötige ich einen Bus vom Hainholzweg", 
        "assert": {
            "start": "Eißendorfer Straße",
            "start_aoi": None,
            "dest": "Vahrenwinkelweg",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich brauche einen Bus von der Zweitbrückenstraße nach St.Pauli", 
        "assert": {
            "start": "Zweitbrückenstraße",
            "start_aoi": None,
            "dest": "St.Pauli",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich bin gerade an der TU Hamburg und muss in 10 Minuten zur Mönckebergstraße", 
        "assert": {
            "start": "TU Hamburg",
            "start_aoi": None,
            "dest": "Mönckebergstraße",
            "dest_aoi": None,
            "date": "today", 
            "time": "now + 10m",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich möchte zum Hafen. Wann geht der Nächste Bus?", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Hafen",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Wann geht die nächste Linue zum Wasser?", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Wasser",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich möchte zur Allianz Arena. Wie komme ich dahin?", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Allianz Arena",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich möchte zur Allianz Arena. Wie komme ich dahin?", 
        "assert": {
            "start": None,
            "start_aoi": None,
            "dest": "Allianz Arena",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": None  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich brauche die schnellste Bus Route vom Kressenweg zum Eppendorfer Marktplatz", 
        "assert": {
            "start": "Kressenweg",
            "start_aoi": None,
            "dest": "Eppendorfer Marktplatz",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Schnellste Bus-Route von der Fähre bis zum Hauptbahnhof", 
        "assert": {
            "start": "Fähre",
            "start_aoi": None,
            "dest": "Hauptbahnhof",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
{ 
    "vars": {
        "anfrage": "Ich habe Lust etwas Neues zu erleben. Letztes Wochenende war ich am Hafen. Da möchte ich heute nicht hin. Mhm. Haha. Ich glaube ich möchte zum HSV Stadium. Da ist es immer sehr schön. Am Besten jetzt gleich, direkt hier von der Brandenburger Straße mit dem Bus", 
        "assert": {
            "start": "Brandenburger Straße",
            "start_aoi": None,
            "dest": "HSV Stadium",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"  
        }
    }
},
]


def generate_tests():
    return test_cases