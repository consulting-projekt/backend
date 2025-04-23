import pandas as pd

test_cases = [
    { 
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
            "assert": {
                "start": None,
                "start_aoi": None,
                "dest": "Innenstadt",
                "dest_aoi": None
            }
        }
    }, 
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zu einem Restarurant in Nähe vom Hafen?", 
            "assert": {
                "start": "Herthastraße",
                "start_aoi": None,
                "dest": "Restarurant",
                "dest_aoi": "Hafen"
            }
        }
    },
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zur Innenstadt?", 
            "assert": {
                "start": "Herthastraße",
                "start_aoi": None,
                "dest": "Innenstadt",
                "dest_aoi": None
            }
        }
    },
    # generiert von claude passend zu verfügbaren daten:
    {
        "vars": {
            "anfrage": "Ich möchte vom U Mümmelmannsberg zu einem Jugendzentrum in der Nähe der Speicherstadt fahren.",
            "assert": {
                "start": "U Mümmelmannsberg",
                "start_aoi": None,
                "dest": "Jugendzentrum",
                "dest_aoi": "Speicherstadt"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Billwerder Ring zur nächsten Behörde?",
            "assert": {
                "start": "Billwerder Ring",
                "start_aoi": None,
                "dest": "Behörde",
                "dest_aoi": None
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wann fährt der nächste Bus vom Bahnhof Bergedorf zum S Allermöhe?",
            "assert": {
                "start": "Bahnhof Bergedorf",
                "start_aoi": None,
                "dest": "S Allermöhe",
                "dest_aoi": None
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom U Steinfurther Allee zum nächsten Jugendzentrum im Stadtteil Billstedt?",
            "assert": {
                "start": "U Steinfurther Allee",
                "start_aoi": None,
                "dest": "Jugendzentrum",
                "dest_aoi": "Billstedt"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Zeige mir den Weg von der Kirchdorfer Straße zur Bücherhalle in der Nähe der Hafencity.",
            "assert": {
                "start": "Kirchdorfer Straße",
                "start_aoi": None,
                "dest": "Bücherhalle",
                "dest_aoi": "Hafencity"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Verbindung von der Davidwache zum Haus der Familie am Elbstrand.",
            "assert": {
                "start": "Davidwache",
                "start_aoi": None,
                "dest": "Haus der Familie",
                "dest_aoi": "Elbstrand"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre von S Billwerder-Moorfleet zur Grundschule in Allermöhe.",
            "assert": {
                "start": "S Billwerder-Moorfleet",
                "start_aoi": None,
                "dest": "Grundschule",
                "dest_aoi": "Allermöhe"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Von Bahnhof Bergedorf zur Freiwilligen Feuerwehr in der Nähe des Curslacker Deichs.",
            "assert": {
                "start": "Bahnhof Bergedorf",
                "start_aoi": None,
                "dest": "Freiwilligen Feuerwehr",
                "dest_aoi": "Curslacker Deich"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre vom Billwerder Billdeich zum Bürgerhaus im Stadtteil Wilhelmsburg.",
            "assert": {
                "start": "Billwerder Billdeich",
                "start_aoi": None,
                "dest": "Bürgerhaus",
                "dest_aoi": "Wilhelmsburg"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Bezirksamt Bergedorf zum Krankenhaus in der Nähe vom Boberger Drift?",
            "assert": {
                "start": "Bezirksamt Bergedorf",
                "start_aoi": None,
                "dest": "Krankenhaus",
                "dest_aoi": "Boberger Drift"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Ich möchte vom U Mümmelmannsberg zum Finanzamt in der Nähe der Mundsburg fahren.",
            "assert": {
                "start": "U Mümmelmannsberg",
                "start_aoi": None,
                "dest": "Finanzamt",
                "dest_aoi": "Mundsburg"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Zeig mir den schnellsten Weg von der Elbchaussee zum Museum am Alsterufer.",
            "assert": {
                "start": "Elbchaussee",
                "start_aoi": None,
                "dest": "Museum",
                "dest_aoi": "Alsterufer"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Verbindung von S Nettelnburg zum Spielplatz im Friedrich-Frank-Bogen.",
            "assert": {
                "start": "S Nettelnburg",
                "start_aoi": None,
                "dest": "Spielplatz",
                "dest_aoi": "Friedrich-Frank-Bogen"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie gelange ich von Billwerder-Moorfleet zum Schwimmbad in Bergedorf?",
            "assert": {
                "start": "Billwerder-Moorfleet",
                "start_aoi": None,
                "dest": "Schwimmbad",
                "dest_aoi": "Bergedorf"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre vom S Billwerder-Moorfleet zur Kirche in Kirchdorf-Süd.",
            "assert": {
                "start": "S Billwerder-Moorfleet",
                "start_aoi": None,
                "dest": "Kirche",
                "dest_aoi": "Kirchdorf-Süd"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Route von Neuengammer Hausdeich zum Job-Center bei der Agentur für Arbeit Harburg.",
            "assert": {
                "start": "Neuengammer Hausdeich",
                "start_aoi": None,
                "dest": "Job-Center",
                "dest_aoi": "Agentur für Arbeit Harburg"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Rathaus Bergedorf zur Grundschule am Friedrich-Frank-Bogen?",
            "assert": {
                "start": "Rathaus Bergedorf",
                "start_aoi": None,
                "dest": "Grundschule",
                "dest_aoi": "Friedrich-Frank-Bogen"
            }
        }
    }
]


def generate_tests():
    return test_cases