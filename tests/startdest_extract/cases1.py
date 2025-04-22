import pandas as pd

# start und dest types = ["adress", "poi_or_aoi",  "station" , None]
test_cases = [
    { 
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
            "assert": {
                "start": [],
                "start_typ": [],
                "dest": ["Innenstadt"],
                "ziel_typ": ["poi_or_aoi"]
            }
        }
    }, 
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zu einem Restarurant in Nähe vom Hafen?", 
            "assert": {
                "start": ["Herthastraße"],
                "start_typ": ["adress"],
                "dest": ["Restarurant", "Hafen"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zur Innenstadt?", 
            "assert": {
                "start": ["Herthastraße"],
                "start_typ": ["adress"],
                "dest": ["Innenstadt"],
                "ziel_typ": ["poi_or_aoi"]
            }
        }
    },
    # generiert von claude passend zu verfügbaren daten:
    {
        "vars": {
            "anfrage": "Ich möchte vom U Mümmelmannsberg zu einem Jugendzentrum in der Nähe der Speicherstadt fahren.",
            "assert": {
                "start": ["U Mümmelmannsberg"],
                "start_typ": ["station"],
                "dest": ["Jugendzentrum", "Speicherstadt"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Billwerder Ring zur nächsten Behörde oder einem Bezirksamt?",
            "assert": {
                "start": ["Billwerder Ring"],
                "start_typ": ["adress"],
                "dest": ["Behörde", "Bezirksamt"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wann fährt der nächste Bus vom Bahnhof Bergedorf zum S Allermöhe?",
            "assert": {
                "start": ["Bahnhof Bergedorf"],
                "start_typ": ["station"],
                "dest": ["S Allermöhe"],
                "ziel_typ": ["station"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom U Steinfurther Allee zum nächsten Jugendzentrum im Stadtteil Billstedt?",
            "assert": {
                "start": ["U Steinfurther Allee"],
                "start_typ": ["station"],
                "dest": ["Jugendzentrum", "Billstedt"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Zeige mir den Weg von der Kirchdorfer Straße zur Bücherhalle in der Nähe der Hafencity.",
            "assert": {
                "start": ["Kirchdorfer Straße"],
                "start_typ": ["adress"],
                "dest": ["Bücherhalle", "Hafencity"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Verbindung von der Davidwache zum Haus der Familie am Elbstrand.",
            "assert": {
                "start": ["Davidwache"],
                "start_typ": ["poi_or_aoi"],
                "dest": ["Haus der Familie", "Elbstrand"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre von S Billwerder-Moorfleet zur Grundschule in Allermöhe.",
            "assert": {
                "start": ["S Billwerder-Moorfleet"],
                "start_typ": ["station"],
                "dest": ["Grundschule", "Allermöhe"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Von Bahnhof Bergedorf zur Freiwilligen Feuerwehr in der Nähe des Curslacker Deichs.",
            "assert": {
                "start": ["Bahnhof Bergedorf"],
                "start_typ": ["station"],
                "dest": ["Freiwilligen Feuerwehr", "Curslacker Deich"],
                "ziel_typ": ["poi_or_aoi", "adress"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre vom Billwerder Billdeich zum Bürgerhaus im Stadtteil Wilhelmsburg.",
            "assert": {
                "start": ["Billwerder Billdeich"],
                "start_typ": ["adress"],
                "dest": ["Bürgerhaus", "Wilhelmsburg"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Bezirksamt Bergedorf zum Krankenhaus in der Nähe vom Boberger Drift?",
            "assert": {
                "start": ["Bezirksamt Bergedorf"],
                "start_typ": ["poi_or_aoi"],
                "dest": ["Krankenhaus", "Boberger Drift"],
                "ziel_typ": ["poi_or_aoi", "adress"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Ich möchte vom U Mümmelmannsberg zum Finanzamt in der Nähe der Mundsburg fahren.",
            "assert": {
                "start": ["U Mümmelmannsberg"],
                "start_typ": ["station"],
                "dest": ["Finanzamt", "Mundsburg"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Zeig mir den schnellsten Weg von der Elbchaussee zum Museum am Alsterufer.",
            "assert": {
                "start": ["Elbchaussee"],
                "start_typ": ["adress"],
                "dest": ["Museum", "Alsterufer"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Verbindung von S Nettelnburg zum Spielplatz im Friedrich-Frank-Bogen.",
            "assert": {
                "start": ["S Nettelnburg"],
                "start_typ": ["station"],
                "dest": ["Spielplatz", "Friedrich-Frank-Bogen"],
                "ziel_typ": ["poi_or_aoi", "adress"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie gelange ich von Billwerder-Moorfleet zum Schwimmbad in Bergedorf?",
            "assert": {
                "start": ["Billwerder-Moorfleet"],
                "start_typ": ["station"],
                "dest": ["Schwimmbad", "Bergedorf"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre vom S Billwerder-Moorfleet zur Kirche in Kirchdorf-Süd.",
            "assert": {
                "start": ["S Billwerder-Moorfleet"],
                "start_typ": ["station"],
                "dest": ["Kirche", "Kirchdorf-Süd"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Route von Neuengammer Hausdeich zum Job-Center bei der Agentur für Arbeit Harburg.",
            "assert": {
                "start": ["Neuengammer Hausdeich"],
                "start_typ": ["adress"],
                "dest": ["Job-Center", "Agentur für Arbeit Harburg"],
                "ziel_typ": ["poi_or_aoi", "poi_or_aoi"]
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Rathaus Bergedorf zur Grundschule am Friedrich-Frank-Bogen?",
            "assert": {
                "start": ["Rathaus Bergedorf"],
                "start_typ": ["poi_or_aoi"],
                "dest": ["Grundschule", "Friedrich-Frank-Bogen"],
                "ziel_typ": ["poi_or_aoi", "adress"]
            }
        }
    }
]


def generate_tests():
    return test_cases