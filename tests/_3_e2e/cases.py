import pandas as pd


test_cases = [
    {
        "vars": {
            "anfrage": "Ich brauche um ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "start": None,
            'answer': "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>." 
            #"answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen dir eine angenehme Fahrt!"
        }
    },
    {
        "vars": {
            "anfrage": "Ich brauche nächste Woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": "Harverdstraße",
            "answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
        }
    },
    {
        "vars": {
            "anfrage": "Wann kommt der nächste Bus in die Innenstadt?",
            "start": None,
            "answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
        }
    },
    {
		"vars": {
			"anfrage": "Wie komme ich jetzt von Lukmoor zu einem Cafe am Hapischtsplatz",
            "start": "Lukmoor",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
	    }
    },
    {
		"vars": {
			"anfrage": "Ich brauche in 2 Stunden einen Zug in die Innenstatt. Gib mir die Route dazu.",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
	    },
	},
    {
		"vars": {
			"anfrage": "Gib mir eine Verbindung zu einem McDonald's in der Inennstadt. Die Ankunft soll 15:00 sein.",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
		}
	},
	{
		"vars": {
			"anfrage": "Ich benötge die nächste Bus-Linie vom Hochrad zu einem Einkaufszentrum in der Nähe des Wintmüllenwegs",
            "start": "Hochrad",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Zeig mir bitte den nächsten Bus von der Station Messberg zu einem Restaurant am Hauptbanhof",
            "start": "Messberg",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich möchte gerne in eine Bar in der Nähe vom Stadtpark. Ich sitze gerade am Ependorfer Martplat und möchte gerne mit dem Bus in 3 Stunden in der Bar sein",
            "start": "Ependorfer Martplat",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "LuftHansa Flughafen -> Roenklobel in ca. 40 min",
            "start": "Flughafen",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich fahre jetzt in Urlaub. Ich brauche einen Bus in 3 Wochen und 5 Tagen um 23 Uhr vom Flughafen zum Prinsenw",
            "start": "Flughafen",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Wie komme ich von der Schnackenburgalle über die Bus Linie 172 zum Volkspark",
            "start": "Schnackenburgalle",
            "answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich muss in eine Bibliothek in St. Pauli. Ich stehe gerade am Hauptbahnhof. Sofort !!!!!!! nur Bus",
            "start": "Hauptbahnhof",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich muss in 2h 35 min von Puckholm zum Rieck Museum. Wie komme ich dort hin?",
            "start": "Puckholm",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich brauche einen Bus von der Zweitbrückenstraße zu einem Park in St.Pauli",
            "start": "Zweitbrückenstraße",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich bin gerade an der TU Hamburg und muss in 10 Minuten zur Mönckebergstraße",
            "start": "TU Hamburg",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich sitze gerade im Loki Schmitt Garden und möchte gerne in 30 minuten in ein Restaurant in der Nähe des Hamburger Hanfens",
            "start": "Loki Schmitt Garden",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich möchte übermorgen zum Hafen. Wie komme ich dort mit dem Bus hin?",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
		}
	},
	{
		"vars": {
			"anfrage": "Wann geht die nächste Linue zum Wasser?",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
		}
	},
	{
		"vars": {
			"anfrage": "Ich möchte in 4 Tagen zur Allianz Arena. Wie komme ich dahin?",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
		}
	},
	{
		"vars": {
			"anfrage": "Schnellste Bus-Route von der Fähre bis zum Hauptbahnhof",
            "start": "Fähre",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich habe Lust etwas Neues zu erleben. Letztes Wochenende war ich am Hafen. Da möchte ich heute nicht hin. Mhm. Haha. Ich glaube ich möchte zum Millerntorstadium. Da ist es immer sehr schön. Am Besten jetzt gleich, direkt hier von der Brandenburger Straße mit dem Bus",
            "start": "Brandenburger Straße",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich habe mein Kind gerade am Rißen - Gymasium abgegeben und möchte nun von hier in 50 Minuten zum Ralstadt - Gymnsium mit Bus bitte",
            "start": "Rißen - Gymasium",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich sitze gerade an der Neuhöfer Str.  und möchte gerne in 3 Stunden in ein Restaurant in der Nähe des SC Nienstedten. Bitte nur den Bus verwenden. Im Zug wird mir immer schlecht.",
            "start": "Neuhöfer Str.",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich sitze gerade am Mö Krill und möchte mit dem Bus zur Elpfilarmonie. Jetzt bitte",
            "start": "Mö Krill",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "in 30 min, Von der Alsterblik zur evang. gemeinde lokstät, das ist in der Nähe von Schilingsbegweg, mit dem bus",
            "start": "Alsterblik",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Zug oder Bus egal, ich muss vom Kanzlershofer Weg zum Seehof",
            "start": "Kanzlershofer Weg",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Morgen um 14 Uhr mi Zug, Graf-Otto-Weg : Pommernweg",
            "start": "Graf-Otto-Weg",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Meine Eltern kommen morgen in die Stadt. Welcher Bus geht vom Gottschalkweg zur Rehkoppel, so ca. 16:30 heute",
            "start": "Gottschalkweg",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "23.07.2025, um 17 Uhr, Manshardstrasse nach Hellmesbergerweg, Zug",
            "start": "Manshardstrasse",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Bus oder zug. Ich muss am 23.Dezember 2026 von der Saseler Straße zu einer Kirche in der Nähe des Skaldenwegs, 5 Uhr morgens",
            "start": "Saseler Straße",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "8 Uhr abends, Wildschwanbrook nach Immenbusch, Bus",
            "start": "Wildschwanbrook",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich muss morgen um 23 Uhr am Kressenweg sein.Fahre von Siloahweg los, mit dem Bus bitte",
            "start": "Siloahweg",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Muss Morgen um 2 Uhr Nachmittags am Eppendorfer Marktplatz sein, Von: Lauenstreinstraße, nur Bus, keine Züge",
            "start": "Lauenstreinstraße",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Wann geht der Nächste Bus zur Station Reeperbahn?",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
		}
	},
	{
		"vars": {
			"anfrage": "Wann geht der nächste Bus der Linie 151 vom Zollamt Waltershof zum Inselpark",
            "start": "Zollamt Waltershof",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Eidelstedter Platz nach Schubackstraße, übermorgen",
            "start": "Eidelstedter Platz",
			"answer": "Die nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich brauche in 35 Minuten einen Bus vom Dörpsweg zur Richardstraße",
            "start": "Dörpsweg",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich muss zur Böttgerstraße",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
		}
	},
	{
		"vars": {
			"anfrage": "Welche Bus-Linie fährt zwischen Suhrenkamp und Röntgenstraße",
            "start": "Suhrenkamp",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich muss morgen zur Grundschule Kirchwerder und wieder zurück",
            "start": None,
			"answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST>."
		}
	},
	{
		"vars": {
			"anfrage": "Ich benötige einen Bus der Linie 543 von der Eißendorfer Straße zum Vahrenwinkelweg. Anschließend benötige ich einen Bus vom Hainholzweg",
            "start": "Eißendorfer Straße",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen? Bitte stelle eine weitere Routenanfrage als separate Nachricht."
		}
	},
	{
		"vars": {
			"anfrage": "Ich benötige einen Bus in 3 Stunden von der Eißendorfer Straße zum Vahrenwinkelweg",
            "start": "Eißendorfer Straße",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
	{
		"vars": {
			"anfrage": "Ich benötige in 8 Tagen einen Bus der Linie 543 von der Eißendorfer Straße zum Vahrenwinkelweg. Anschließend benötige ich einen Bus vom Hainholzweg",
            "start": "Eißendorfer Straße",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen? Bitte stelle eine weitere Routenanfrage als separate Nachricht."
		}
	},
	{
		"vars": {
			"anfrage": "Ich brauche die schnellste Bus Route vom Kressenweg zum Eppendorfer Marktplatz",
            "start": "Kressenweg",
			"answer": "Der nächste <TRANSPORT> <LINE> mit Fahrtrichtung <DIRECTION> startet am <DATE> um <TIME> Uhr von der Haltestelle <START>. Möchtest du noch etwas wissen?"
		}
	},
]


def generate_tests():
    return test_cases
