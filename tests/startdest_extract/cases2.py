import pandas as pd

test_cases = [
    { 
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
            "assert": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Innenstadt",
                "ziel_bedingung": None
            }
        }
    }, 
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zu einem Restarurant in Nähe vom Hafen?", 
            "assert": {
                "start": "Herthastraße",
                "start_bedingung": None,
                "ziel": "Restarurant",
                "ziel_bedingung": "Hafen"
            }
        }
    },
    { 
        "vars": {
            "anfrage": "Zeige mir eine Verbindung von Herthastraße zur Innenstadt?", 
            "assert": {
                "start": "Herthastraße",
                "start_bedingung": None,
                "ziel": "Innenstadt",
                "ziel_bedingung": None
            }
        }
    },
    # generiert von claude passend zu verfügbaren daten:
    {
        "vars": {
            "anfrage": "Ich möchte vom U Mümmelmannsberg zu einem Jugendzentrum in der Nähe der Speicherstadt fahren.",
            "assert": {
                "start": "U Mümmelmannsberg",
                "start_bedingung": None,
                "ziel": "Jugendzentrum",
                "ziel_bedingung": "Speicherstadt"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Billwerder Ring zur nächsten Behörde?",
            "assert": {
                "start": "Billwerder Ring",
                "start_bedingung": None,
                "ziel": "Behörde",
                "ziel_bedingung": None
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wann fährt der nächste Bus vom Bahnhof Bergedorf zum S Allermöhe?",
            "assert": {
                "start": "Bahnhof Bergedorf",
                "start_bedingung": None,
                "ziel": "S Allermöhe",
                "ziel_bedingung": None
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom U Steinfurther Allee zum nächsten Jugendzentrum im Stadtteil Billstedt?",
            "assert": {
                "start": "U Steinfurther Allee",
                "start_bedingung": None,
                "ziel": "Jugendzentrum",
                "ziel_bedingung": "Billstedt"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Zeige mir den Weg von der Kirchdorfer Straße zur Bücherhalle in der Nähe der Hafencity.",
            "assert": {
                "start": "Kirchdorfer Straße",
                "start_bedingung": None,
                "ziel": "Bücherhalle",
                "ziel_bedingung": "Hafencity"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Verbindung von der Davidwache zum Haus der Familie am Elbstrand.",
            "assert": {
                "start": "Davidwache",
                "start_bedingung": None,
                "ziel": "Haus der Familie",
                "ziel_bedingung": "Elbstrand"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre von S Billwerder-Moorfleet zur Grundschule in Allermöhe.",
            "assert": {
                "start": "S Billwerder-Moorfleet",
                "start_bedingung": None,
                "ziel": "Grundschule",
                "ziel_bedingung": "Allermöhe"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Von Bahnhof Bergedorf zur Freiwilligen Feuerwehr in der Nähe des Curslacker Deichs.",
            "assert": {
                "start": "Bahnhof Bergedorf",
                "start_bedingung": None,
                "ziel": "Freiwilligen Feuerwehr",
                "ziel_bedingung": "Curslacker Deich"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre vom Billwerder Billdeich zum Bürgerhaus im Stadtteil Wilhelmsburg.",
            "assert": {
                "start": "Billwerder Billdeich",
                "start_bedingung": None,
                "ziel": "Bürgerhaus",
                "ziel_bedingung": "Wilhelmsburg"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Bezirksamt Bergedorf zum Krankenhaus in der Nähe vom Boberger Drift?",
            "assert": {
                "start": "Bezirksamt Bergedorf",
                "start_bedingung": None,
                "ziel": "Krankenhaus",
                "ziel_bedingung": "Boberger Drift"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Ich möchte vom U Mümmelmannsberg zum Finanzamt in der Nähe der Mundsburg fahren.",
            "assert": {
                "start": "U Mümmelmannsberg",
                "start_bedingung": None,
                "ziel": "Finanzamt",
                "ziel_bedingung": "Mundsburg"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Zeig mir den schnellsten Weg von der Elbchaussee zum Museum am Alsterufer.",
            "assert": {
                "start": "Elbchaussee",
                "start_bedingung": None,
                "ziel": "Museum",
                "ziel_bedingung": "Alsterufer"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Verbindung von S Nettelnburg zum Spielplatz im Friedrich-Frank-Bogen.",
            "assert": {
                "start": "S Nettelnburg",
                "start_bedingung": None,
                "ziel": "Spielplatz",
                "ziel_bedingung": "Friedrich-Frank-Bogen"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie gelange ich von Billwerder-Moorfleet zum Schwimmbad in Bergedorf?",
            "assert": {
                "start": "Billwerder-Moorfleet",
                "start_bedingung": None,
                "ziel": "Schwimmbad",
                "ziel_bedingung": "Bergedorf"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Fahre vom S Billwerder-Moorfleet zur Kirche in Kirchdorf-Süd.",
            "assert": {
                "start": "S Billwerder-Moorfleet",
                "start_bedingung": None,
                "ziel": "Kirche",
                "ziel_bedingung": "Kirchdorf-Süd"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Route von Neuengammer Hausdeich zum Job-Center bei der Agentur für Arbeit Harburg.",
            "assert": {
                "start": "Neuengammer Hausdeich",
                "start_bedingung": None,
                "ziel": "Job-Center",
                "ziel_bedingung": "Agentur für Arbeit Harburg"
            }
        }
    },
    {
        "vars": {
            "anfrage": "Wie komme ich vom Rathaus Bergedorf zur Grundschule am Friedrich-Frank-Bogen?",
            "assert": {
                "start": "Rathaus Bergedorf",
                "start_bedingung": None,
                "ziel": "Grundschule",
                "ziel_bedingung": "Friedrich-Frank-Bogen"
            }
        }
    }
]


def generate_tests():
    return test_cases