import pandas as pd

test_cases = [
    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "assert": {
                "start": None,  # mögliche Werte: None, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben

                # mögliche Werte: None, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
                "dest": "Innenstadt",
                # mögliche Werte: None, <dest aoi> wenn für "dest" adresse|station|poi angegeben
                "dest_aoi": "user_location",
                # mögliche Werte= None, today, today + 3m3w5d (d:Tage, w:Wochen, m:monate), Datum mit Zielformat: 22.04.2025
                "date": "today",
                # mögliche Werte= None, now, now + 3h2m (m:Minuten, h:Stunden), Zeit mit Zielformat: 18:30
                "time": "15:00",
                # mögliche Werte: True, False; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
                "time_is_departure": True,
                "type_of_transport": "bus"  # mögliche Werte: None, bus, train
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Ich brauche nächste woche von der Harvertstraße einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "assert": {
                "start": "Harvertstraße",

                "dest": "Innenstadt",
                "dest_aoi": None,
                "date": "today + 1w",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstatt?",
            "assert": {
                "start": None,

                "dest": "Innenstatt",
                "dest_aoi": "user_location",
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # # Mit Dest_AOI
    {
        "vars": {
            "anfrage": "Wie komme ich jetzt von Lukmoor zu einem Cafe am Hapischtsplatz",
            "assert": {
                "start": "Lukmoor",

                "dest": "Cafe",
                "dest_aoi": "Hapischtsplatz",
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich brauche in 2 Stunden einen Zug in die Innenstatt. Gib mir die Route dazu.",
            "assert": {
                "start": None,

                "dest": "Innenstatt",
                "dest_aoi": "user_location",
                "date": "today",
                "time": "now + 120m",
                "time_is_departure": True,
                "type_of_transport": "train"
            }
        }
    },
    # Embedding Use-Case
    # Mit Dest_AOI
    {
        "vars": {
            "anfrage": "Gib mir eine Verbindung zu einem McDonald's in der Inennstadt. Die Ankunft soll 15:00 sein.",
            "assert": {
                "start": None,

                "dest": "McDonald's",
                "dest_aoi": "Inennstadt",
                "date": "today",
                "time": "15:00",
                "time_is_departure": False,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    # # Mit Dest_AOI
    {
        "vars": {
            "anfrage": "Ich benötge die nächste Bus-Linie vom Hochrad zu einem Einkaufszentrum in der Nähe des Wintmüllenwegs",
            "assert": {
                "start": "Hochrad",

                "dest": "Wintmüllenweg",
                "dest_aoi": "Einkaufszentrum",
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # # Mit Dest_AOI
    {
        "vars": {
            "anfrage": "Zeig mir bitte den nächsten Bus von der Station Messberg zu einem Restaurant am Hauptbanhof",
            "assert": {
                "start": "Messberg",

                "dest": "Restaurant",
                "dest_aoi": "Hauptbanhof",
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Mit Dest_AOI
    # Embedding Use-Case
    # Komplexe Zeitangabe
    #
    {
        "vars": {
            "anfrage": "Ich möchte gerne in eine Bar in der Nähe vom Stadtpark. Ich sitze gerade am Ependorfer Martplat und möchte gerne mit dem Bus in 3 Stunden in der Bar sein",
            "assert": {
                "start": "Ependorfer Martplat",

                "dest": "Bar",
                "dest_aoi": "Stadtpark",
                "date": "today",
                "time": "now + 3h",
                "time_is_departure": False,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "LuftHansa Flughafen -> Roenklobel in ca. 40 min",
            "assert": {
                "start": "Flughafen",

                "dest": "Roenklobel",
                "dest_aoi": None,
                "date": "today",
                "time": "now + 40m",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Ich fahre jetzt in Urlaub. Ich brauche einen Bus in 3 Wochen und 5 Tagen um 23 Uhr vom Flughafen zum Prinsenw",
            "assert": {
                "start": "Flughafen",

                "dest": "Prinsenw",
                "dest_aoi": None,
                "date": "today + 26d",
                "time": "23:00",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Wie komme ich von der Schnackenburgalle über die Bus Linie 172 zum Volkspark",
            "assert": {
                "start": "Schnackenburgalle",

                "dest": "Volkspark",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # Mit Dest_AOI
    {
        "vars": {
            "anfrage": "Ich muss in eine Bibliothek in St. Pauli. Ich stehe gerade am Hauptbahnhof. Sofort !!!!!!! nur Bus",
            "assert": {
                "start": "Hauptbahnhof",

                "dest": "Bibliothek",
                "dest_aoi": "St. Pauli",
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich muss in 2h 35 min von Puckholm zum Rieck Museum. Wie komme ich dort hin?",
            "assert": {
                "start": "Puckholm",

                "dest": "Rieck Museum",
                "dest_aoi": None,
                "date": "today",
                "time": "now + 2h35m",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    # Mit Dest_AOI
    {
        "vars": {
            "anfrage": "Ich brauche einen Bus von der Zweitbrückenstraße zu einem Park in St.Pauli",
            "assert": {
                "start": "Zweitbrückenstraße",

                "dest": "Park",
                "dest_aoi": "St.Pauli",
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich bin gerade an der TU Hamburg und muss in 10 Minuten zur Mönckebergstraße",
            "assert": {
                "start": "TU Hamburg",

                "dest": "Mönckebergstraße",
                "dest_aoi": None,
                "date": "today",
                "time": "now + 10m",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    # Mit Dest_AOI
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich sitze gerade im Loki Schmitt Garden und möchte gerne in 30 minuten in ein Restaurant in der Nähe des Hamburger Hanfens",
            "assert": {
                "start": "Loki Schmitt Garden",

                "dest": "Restaurant",
                "dest_aoi": "Hamburger Hafen",
                "date": "today",
                "time": "now + 30m",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Ich möchte übermorgen zum Hafen. Wie komme ich dort mit dem Bus hin?",
            "assert": {
                "start": None,

                "dest": "Hafen",
                "dest_aoi": "user_location",
                "date": "today + 2d",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Wann geht die nächste Linue zum Wasser?",
            "assert": {
                "start": None,

                "dest": "Wasser",
                "dest_aoi": "user_location",
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Ich möchte in 4 Tagen zur Allianz Arena. Wie komme ich dahin?",
            "assert": {
                "start": None,

                "dest": "Allianz Arena",
                "dest_aoi": "user_location",
                "date": "today + 4d",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Schnellste Bus-Route von der Fähre bis zum Hauptbahnhof",
            "assert": {
                "start": "Fähre",

                "dest": "Hauptbahnhof",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Ich habe Lust etwas Neues zu erleben. Letztes Wochenende war ich am Hafen. Da möchte ich heute nicht hin. Mhm. Haha. Ich glaube ich möchte zum Millerntorstadium. Da ist es immer sehr schön. Am Besten jetzt gleich, direkt hier von der Brandenburger Straße mit dem Bus",
            "assert": {
                "start": "Brandenburger Straße",

                "dest": "Millerntorstadium",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich habe mein Kind gerade am Rißen - Gymasium abgegeben und möchte nun von hier in 50 Minuten zum Ralstadt - Gymnsium mit Bus bitte",
            "assert": {
                "start": "Rißen - Gymasium",

                "dest": "Ralstadt - Gymnsium",
                "dest_aoi": None,
                "date": "today",
                "time": "now + 50m",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # Mit Dest_AOI
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich sitze gerade an der Neuhöfer Str.  und möchte gerne in 3 Stunden in ein Restaurant in der Nähe des SC Nienstedten. Bitte nur den Bus verwenden. Im Zug wird mir immer schlecht.",
            "assert": {
                "start": "Neuhöfer Str.",

                "dest": "Restaurant",
                "dest_aoi": "SC Nienstedten",
                "date": "today",
                "time": "now + 3h",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },

    # Embedding Use-Case
    {
        "vars": {
            "anfrage": "Ich sitze gerade am Mö Krill und möchte mit dem Bus zur Elpfilarmonie. Jetzt bitte",
            "assert": {
                "start": "Mö Krill",

                "dest": "Elpfilarmonie",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Embedding Use-Case
    # Mit Dest_AOI
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "in 30 min, Von der Alsterblik zur evang. gemeinde lokstät, das ist in der Nähe von Schilingsbegweg, mit dem bus",
            "assert": {
                "start": "Alsterblik",

                "dest": "evang. gemeinde lokstät",
                "dest_aoi": "Schilingsbegweg",
                "date": "today",
                "time": "now + 30m",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Zug oder Bus egal, ich muss vom Kanzlershofer Weg zum Seehof",
            "assert": {
                "start": "Kanzlershofer Weg",

                "dest": "Seehof",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Morgen um 14 Uhr mi Zug, Graf-Otto-Weg : Pommernweg",
            "assert": {
                "start": "Graf-Otto-Weg",

                "dest": "Pommernweg",
                "dest_aoi": None,
                "date": "today + 1d",
                "time": "14:00",
                "time_is_departure": True,
                "type_of_transport": "train"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Meine Eltern kommen morgen in die Stadt. Welcher Bus geht vom Gottschalkweg zur Rehkoppel, so ca. 16:30 heute",
            "assert": {
                "start": "Gottschalkweg",

                "dest": "Rehkoppel",
                "dest_aoi": None,
                "date": "today",
                "time": "16:30",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "23.07.2025, um 17 Uhr, Manshardstrasse nach Hellmesbergerweg, Zug",
            "assert": {
                "start": "Manshardstrasse",

                "dest": "Hellmesbergerweg",
                "dest_aoi": None,
                "date": "23.07.2025",
                "time": "17:00",
                "time_is_departure": True,
                "type_of_transport": "train"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Bus oder zug. Ich muss am 23.Dezember 2026 von der Saseler Straße zu einer Kirche in der Nähe des Skaldenwegs, 5 Uhr morgens",
            "assert": {
                "start": "Saseler Straße",

                "dest": "Kirche",
                "dest_aoi": "Skaldenweg",
                "date": "23.12.2026",
                "time": "05:00",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "8 Uhr abends, Wildschwanbrook nach Immenbusch, Bus",
            "assert": {
                "start": "Wildschwanbrook",

                "dest": "Immenbusch",
                "dest_aoi": None,
                "date": "today",
                "time": "20:00",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Ich muss morgen um 23 Uhr am Kressenweg sein.Fahre von Siloahweg los, mit dem Bus bitte",
            "assert": {
                "start": "Siloahweg",

                "dest": "Kressenweg",
                "dest_aoi": None,
                "date": "today + 1d",
                "time": "23:00",
                "time_is_departure": False,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Muss Morgen um 2 Uhr Nachmittags am Eppendorfer Marktplatz sein, Von: Lauenstreinstraße, nur Bus, keine Züge",
            "assert": {
                "start": "Lauenstreinstraße",

                "dest": "Eppendorfer Marktplatz",
                "dest_aoi": None,
                "date": "today + 1d",
                "time": "14:00",
                "time_is_departure": False,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Wann geht der Nächste Bus zur Station Reeperbahn?",
            "assert": {
                "start": None,

                "dest": "Reeperbahn",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Wann geht der nächste Bus der Linie 151 vom Zollamt Waltershof zum Inselpark",
            "assert": {
                "start": "Zollamt Waltershof",

                "dest": "Inselpark",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Eidelstedter Platz nach Schubackstraße, übermorgen",
            "assert": {
                "start": "Eidelstedter Platz",

                "dest": "Schubackstraße",
                "dest_aoi": None,
                "date": "today + 2d",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich brauche in 35 Minuten einen Bus vom Dörpsweg zur Richardstraße",
            "assert": {
                "start": "Dörpsweg",

                "dest": "Richardstraße",
                "dest_aoi": None,
                "date": "today",
                "time": "now + 35m",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Ich muss zur Böttgerstraße",
            "assert": {
                "start": None,

                "dest": "Böttgerstraße",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Welche Bus-Linie fährt zwischen Suhrenkamp und Röntgenstraße",
            "assert": {
                "start": "Suhrenkamp",

                "dest": "Röntgenstraße",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Ich muss morgen zur Grundschule Kirchwerder und wieder zurück",
            "assert": {
                "start": None,

                "dest": "Grundschule Kirchwerder",
                "dest_aoi": None,
                "date": "today + 1d",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": None
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Ich benötige einen Bus der Linie 543 von der Eißendorfer Straße zum Vahrenwinkelweg. Anschließend benötige ich einen Bus vom Hainholzweg",
            "assert": {
                "start": "Eißendorfer Straße",

                "dest": "Vahrenwinkelweg",
                "dest_aoi": None,
                "date": "today",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Zeitangabe
    {
        "vars": {
            "anfrage": "Ich benötige einen Bus in 3 Stunden von der Eißendorfer Straße zum Vahrenwinkelweg",
            "assert": {
                "start": "Eißendorfer Straße",

                "dest": "Vahrenwinkelweg",
                "dest_aoi": None,
                "date": "today",
                "time": "now + 3h",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    # Komplexe Datumsangabe
    {
        "vars": {
            "anfrage": "Ich benötige in 8 Tagen einen Bus der Linie 543 von der Eißendorfer Straße zum Vahrenwinkelweg. Anschließend benötige ich einen Bus vom Hainholzweg",
            "assert": {
                "start": "Eißendorfer Straße",

                "dest": "Vahrenwinkelweg",
                "dest_aoi": None,
                "date": "today + 8d",
                "time": "now",
                "time_is_departure": True,
                "type_of_transport": "bus"
            }
        }
    },
    # Direkter GeoFox API Abruf
    {
        "vars": {
            "anfrage": "Ich brauche die schnellste Bus Route vom Kressenweg zum Eppendorfer Marktplatz",
            "assert": {
                "start": "Kressenweg",

                "dest": "Eppendorfer Marktplatz",
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
