import pandas as pd

# start und dest types = ["adress", "poi_or_aoi",  "station" , None]
test_cases = [
    { 
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Kirche",
                "ziel_bedingung": "Kirchdorf-Süd"
            }, 
            "assert": {
                "ziel_name_contains": ["Kirche"],
                "ziel_nahe": "POINT(10.020014 53.483826)"
            }
        }
    }, 
    
    # "Wann kommt der nächste Bus in die Innenstadt?"
    { 
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Innenstadt",
                "ziel_bedingung": None
            }, 
            "assert": {
                "ziel_name_contains": ["Innenstadt"]
            }
        }
    },
    
    # "Zeige mir eine Verbindung von Herthastraße zu einem Restarurant in Nähe vom Hafen?"
    { 
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Restarurant",
                "ziel_bedingung": "Hafen"
            }, 
            "assert": {
                "ziel_name_contains": ["Restaurant"],
                "ziel_nahe": "POINT(9.9800 53.5450)"  # Ungefähre Koordinaten für Hamburger Hafen
            }
        }
    },
    
    # "Zeige mir eine Verbindung von Herthastraße zur Innenstadt?"
    { 
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Innenstadt",
                "ziel_bedingung": None
            }, 
            "assert": {
                "ziel_name_contains": ["Innenstadt"]
            }
        }
    },
    
    # "Ich möchte vom U Mümmelmannsberg zu einem Jugendzentrum in der Nähe der Speicherstadt fahren."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Jugendzentrum",
                "ziel_bedingung": "Speicherstadt"
            },
            "assert": {
                "ziel_name_contains": ["Jugendzentrum"],
                "ziel_nahe": "POINT(9.9877 53.5456)"  # Ungefähre Koordinaten für Speicherstadt
            }
        }
    },
    
    # "Wie komme ich vom Billwerder Ring zur nächsten Behörde?"
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Behörde",
                "ziel_bedingung": None
            },
            "assert": {
                "ziel_name_contains": ["Behörde", "Amt", "Verwaltung"]
            }
        }
    },
    
    # "Wann fährt der nächste Bus vom Bahnhof Bergedorf zum S Allermöhe?"
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": None,
                "ziel_bedingung": None
            },
            "assert": {}  # Beide sind Stationen, nicht in Qdrant vorhanden
        }
    },
    
    # "Wie komme ich vom U Steinfurther Allee zum nächsten Jugendzentrum im Stadtteil Billstedt?"
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Jugendzentrum",
                "ziel_bedingung": "Billstedt"
            },
            "assert": {
                "ziel_name_contains": ["Jugendzentrum"],
                "ziel_nahe": "POINT(10.1065 53.5559)"  # Ungefähre Koordinaten für Billstedt
            }
        }
    },
    
    # "Zeige mir den Weg von der Kirchdorfer Straße zur Bücherhalle in der Nähe der Hafencity."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Bücherhalle",
                "ziel_bedingung": "Hafencity"
            },
            "assert": {
                "ziel_name_contains": ["Bücherhalle", "Bibliothek"],
                "ziel_nahe": "POINT(10.0041 53.5414)"  # Ungefähre Koordinaten für Hafencity
            }
        }
    },
    
    # "Verbindung von der Davidwache zum Haus der Familie am Elbstrand."
    {
        "vars": {
            "anfrage": {
                "start": "Davidwache",
                "start_bedingung": None,
                "ziel": "Haus der Familie",
                "ziel_bedingung": "Elbstrand"
            },
            "assert": {
                "start_name_contains": ["Davidwache", "Polizei"],
                "ziel_name_contains": ["Haus der Familie"],
                "ziel_nahe": "POINT(9.8950 53.5430)"  # Ungefähre Koordinaten für Elbstrand
            }
        }
    },
    
    # "Fahre von S Billwerder-Moorfleet zur Grundschule in Allermöhe."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Grundschule",
                "ziel_bedingung": "Allermöhe"
            },
            "assert": {
                "ziel_name_contains": ["Grundschule", "Schule"],
                "ziel_nahe": "POINT(10.1500 53.5070)"  # Ungefähre Koordinaten für Allermöhe
            }
        }
    },
    
    # "Von Bahnhof Bergedorf zur Freiwilligen Feuerwehr in der Nähe des Curslacker Deichs."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Freiwilligen Feuerwehr",
                "ziel_bedingung": "Curslacker Deich"
            },
            "assert": {
                "ziel_name_contains": ["Feuerwehr"],
                "ziel_nahe": "POINT(10.2000 53.4800)"  # Ungefähre Koordinaten für Curslacker Deich
            }
        }
    },
    
    # "Fahre vom Billwerder Billdeich zum Bürgerhaus im Stadtteil Wilhelmsburg."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Bürgerhaus",
                "ziel_bedingung": "Wilhelmsburg"
            },
            "assert": {
                "ziel_name_contains": ["Bürgerhaus"],
                "ziel_nahe": "POINT(9.9900 53.5000)"  # Ungefähre Koordinaten für Wilhelmsburg
            }
        }
    },
    
    # "Wie komme ich vom Bezirksamt Bergedorf zum Krankenhaus in der Nähe vom Boberger Drift?"
    {
        "vars": {
            "anfrage": {
                "start": "Bezirksamt Bergedorf",
                "start_bedingung": None,
                "ziel": "Krankenhaus",
                "ziel_bedingung": "Boberger Drift"
            },
            "assert": {
                "start_name_contains": ["Bezirksamt", "Bergedorf"],
                "ziel_name_contains": ["Krankenhaus"],
                "ziel_nahe": "POINT(10.1800 53.5100)"  # Ungefähre Koordinaten für Boberger Drift
            }
        }
    },
    
    # "Ich möchte vom U Mümmelmannsberg zum Finanzamt in der Nähe der Mundsburg fahren."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Finanzamt",
                "ziel_bedingung": "Mundsburg"
            },
            "assert": {
                "ziel_name_contains": ["Finanzamt"],
                "ziel_nahe": "POINT(10.0300 53.5700)"  # Ungefähre Koordinaten für Mundsburg
            }
        }
    },
    
    # "Zeig mir den schnellsten Weg von der Elbchaussee zum Museum am Alsterufer."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Museum",
                "ziel_bedingung": "Alsterufer"
            },
            "assert": {
                "ziel_name_contains": ["Museum"],
                "ziel_nahe": "POINT(9.9982 53.5653)"  # Ungefähre Koordinaten für Alsterufer
            }
        }
    },
    
    # "Verbindung von S Nettelnburg zum Spielplatz im Friedrich-Frank-Bogen."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Spielplatz",
                "ziel_bedingung": "Friedrich-Frank-Bogen"
            },
            "assert": {
                "ziel_name_contains": ["Spielplatz"],
                "ziel_nahe": "POINT(10.1710 53.4900)"  # Ungefähre Koordinaten für Friedrich-Frank-Bogen
            }
        }
    },
    
    # "Wie gelange ich von Billwerder-Moorfleet zum Schwimmbad in Bergedorf?"
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Schwimmbad",
                "ziel_bedingung": "Bergedorf"
            },
            "assert": {
                "ziel_name_contains": ["Schwimmbad", "Schwimmhalle", "Bad"],
                "ziel_nahe": "POINT(10.2000 53.4900)"  # Ungefähre Koordinaten für Bergedorf
            }
        }
    },
    # "Route von Neuengammer Hausdeich zum Job-Center bei der Agentur für Arbeit Harburg."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_bedingung": None,
                "ziel": "Job-Center",
                "ziel_bedingung": "Agentur für Arbeit Harburg"
            },
            "assert": {
                "ziel_name_contains": ["Job-Center", "Jobcenter", "Agentur für Arbeit"],
                "ziel_nahe": "POINT(9.9775 53.4601)"  # Ungefähre Koordinaten für Harburg
            }
        }
    },
    # "Wie komme ich vom Rathaus Bergedorf zur Grundschule am Friedrich-Frank-Bogen?"
    {
        "vars": {
            "anfrage": {
                "start": "Rathaus Bergedorf",
                "start_bedingung": None,
                "ziel": "Grundschule",
                "ziel_bedingung": "Friedrich-Frank-Bogen"
            },
            "assert": {
                "start_name_contains": ["Rathaus", "Bergedorf"],
                "ziel_name_contains": ["Grundschule", "Schule"],
                "ziel_nahe": "POINT(10.1710 53.4900)"  # Ungefähre Koordinaten für Friedrich-Frank-Bogen
            }
        }
    }
]


def generate_tests():
    return test_cases