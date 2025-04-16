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
                "ziel_nahe": ["POINT(10.000413 53.554069)", 1000]
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
                "ziel_nahe": ["POINT(9.988080668856236 53.55184559306223)", 5000]
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
                "ziel_nahe": ["POINT(9.984983833154688 53.47308499617683)", 5000]
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
                "ziel_nahe":  ["POINT(9.988080668856236 53.55184559306223)", 5000]
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
                "ziel_nahe": ["POINT(10.00467865 53.54357754999999)", 5000]
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
                "ziel_name_contains": ["Behörde", "Amt", "Verwaltung"],
                "ziel_nahe": ["POINT(9.984663 53.554245)", 5000]
            }
        }
    }, # "Wie komme ich vom U Steinfurther Allee zum nächsten Jugendzentrum im Stadtteil Billstedt?"
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
                "ziel_nahe": ["POINT(10.104508884450647 53.54136343631377)", 5000]  # Ungefähre Koordinaten für Billstedt
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
                "ziel_nahe":  ["POINT(9.994725 53.541915)", 5000]  # Ungefähre Koordinaten für Hafencity
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
                "ziel_nahe": ["POINT(9.96242186569669 53.557507857835716)", 5000]  # Ungefähre Koordinaten für Elbstrand
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
                "ziel_nahe":["POINT(10.160813 53.486764)", 5000] # Ungefähre Koordinaten für Allermöhe
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
                "ziel_nahe": ["POINT(9.793617541260351 53.514917074226595)", 5000]  # Ungefähre Koordinaten für Curslacker Deich
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
                "ziel_nahe": ["POINT(9.995909203025185 53.50033548012308)", 5000]  # Ungefähre Koordinaten für Wilhelmsburg
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
                "ziel_nahe": ["POINT(10.152339730730844 53.513922532693044)", 5000]  # Ungefähre Koordinaten für Boberger Drift
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
                "ziel_nahe": ["POINT(10.00333 53.550451)", 5000] # Ungefähre Koordinaten für Mundsburg
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
                "ziel_nahe": ["POINT(10.001416935070356 53.56763769598505)", 5000]  # Ungefähre Koordinaten für Alsterufer
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
                "ziel_nahe": ["POINT(10.178885799999998 53.49181495)", 5000]  # Ungefähre Koordinaten für Friedrich-Frank-Bogen
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
                "ziel_nahe": ["POINT(10.220398 53.487293)", 5000] # Ungefähre Koordinaten für Bergedorf
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
                "ziel_nahe": ["POINT(9.978567 53.460712)", 5000]  # Ungefähre Koordinaten für Harburg
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
                "ziel_nahe": ["POINT(10.178885799999998 53.49181495)", 5000]  # Ungefähre Koordinaten für Friedrich-Frank-Bogen
            }
        }
    }
]


def generate_tests():
    return test_cases


if __name__ == "__main__":
    # Example usage
    import ast
    test_cases = generate_tests()
    for case in test_cases:
        anfrage =  case["vars"]["anfrage"]
        anfrage_fromstr = ast.literal_eval(str(anfrage).strip())
        print(f"From str: {anfrage_fromstr}")