import pandas as pd

# start und dest types = ["adress", "poi_or_aoi",  "station" , None]
test_cases = [
    { 
        "vars": {
            "anfrage": {
                "start": None, # point of interest oder area of interest
                "start_aoi": None, # immer eine area of interest
                "dest": "Kirche", # point of interest oder area of interest
                "dest_aoi": "Kirchdorf-Süd" # immer eine area of interest
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
                "start_aoi": None,
                "dest": "Innenstadt",
                "dest_aoi": None
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
                "start_aoi": None,
                "dest": "Restarurant",
                "dest_aoi": "Hafen"
            }, 
            "assert": {
                "ziel_nahe": ["POINT(9.984983833154688 53.47308499617683)", 5000]
            }
        }
    },
    
    
    # "Ich möchte vom U Mümmelmannsberg zu einem Jugendzentrum in der Nähe der Speicherstadt fahren."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_aoi": None,
                "dest": "Jugendzentrum",
                "dest_aoi": "Speicherstadt"
            },
            "assert": {
                "ziel_nahe": ["POINT(10.00467865 53.54357754999999)", 5000]
            }
        }
    },
    
     # "Wie komme ich vom U Steinfurther Allee zum nächsten Jugendzentrum im Stadtteil Billstedt?"
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_aoi": None,
                "dest": "Jugendzentrum",
                "dest_aoi": "Billstedt"
            },
            "assert": {
                "ziel_name_contains": ["Jugend"],
                "ziel_nahe": ["POINT(10.104508884450647 53.54136343631377)", 5000]  # Ungefähre Koordinaten für Billstedt
            }
        }
    },
    
    # "Zeige mir den Weg von der Kirchdorfer Straße zur Bücherhalle in der Nähe der Hafencity."
    {
        "vars": {
            "anfrage": {
                "start": None,
                "start_aoi": None,
                "dest": "Bücherhalle",
                "dest_aoi": "Hafencity"
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
                "start_aoi": None,
                "dest": "Haus der Familie",
                "dest_aoi": "Elbstrand"
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
                "start_aoi": None,
                "dest": "Grundschule",
                "dest_aoi": "Allermöhe"
            },
            "assert": {
                "ziel_name_contains": ["Grundschule", "Schule"],
                "ziel_nahe":["POINT(10.160813 53.486764)", 5000] # Ungefähre Koordinaten für Allermöhe
            }
        }
    },

    # LuftHansa Flughafen -> Rönkloppel in ca. 40 min
    {
        "vars": {
            "anfrage": {
                "start": "Flughafen",
                "start_aoi": None,
                "dest": "Rönkloppel",
                "dest_aoi": None,
            },
            "assert": {
                "start_name_contains": ["Airport", "Flughafen"],
                "start_nahe":["POINT(10.006270459777692 53.63228460547464)", 7000]
            }
        }
    },
    # Wie komme ich von der Schnackenburgalle über die Bus Linie 172 zum Volkspark
    {
        "vars": {
            "anfrage": {
                "start": "Schnackenburgalle",
                "start_aoi": None,
                "dest": "Volkspark",
                "dest_aoi": None,
            },
            "assert": {
                "ziel_name_contains": ["Park", "Volkspark"],
                "ziel_nahe":["POINT(9.901091676352436 53.58340196584053)", 2000]
            }
        }
    },
    # Ich muss in 2h 35 min von Puckholm zum Rieck Museum. Wie komme ich dort hin?
    {
        "vars": {
            "anfrage": {
                "start": "Puckholm",
                "start_aoi": None,
                "dest": "Rieck Museum",
                "dest_aoi": None,
            },
            "assert": {
                "ziel_name_contains": ["Museum", "Rieck Haus"],
                "ziel_nahe":["POINT(10.214631390056974 53.45938998698139)", 5000]
            }
        }
    },
     # Ich brauche einen Bus von der Zweitbrückenstraße nach St.Pauli"
    {
        "vars": {
            "anfrage": {
                "start": "Zweitbrückenstraße",
                "start_aoi": None,
                "dest": "St.Pauli",
                "dest_aoi": None,
            },
            "assert": {
                "ziel_name_contains": ["St. Pauli"],
                "ziel_nahe":["POINT(9.96991127111408 53.5509767798889)", 2000]
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