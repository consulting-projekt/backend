from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
import json
import pprint
import re

from src.utils_llm import call_phi_4




def call_api(prompt, options, context):
    return {
        "output": call_phi_4(prompt),
    }




if __name__ == "__main__":
    # Example usage
    prompt = """
Du bist ein experte im öffentlichen Nahverkehr und hast die Aufgabe basierend auf einer Nutzeranfrage folgende entities zu extrahieren:

"start": mögliche Werte= null, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
"dest":  mögliche Werte= null, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
"dest_aoi":  mögliche Werte= null, <dest aoi> wenn für "dest" adresse|station|poi angegeben
"date":  mögliche Werte= null, today, today + 3m3w5d (d:Tage, w:Wochen, m:monate), Datum mit Zielformat: 22.04.2025
"time": mögliche Werte= null, now, now + 3h2m (m:Minuten, h:Stunden), Zeit mit Zielformat: 18:30
"time_is_departure":  mögliche Werte= true, false; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
"type_of_transport":  mögliche Werte= null, bus, train

Für die Bestimmung der Werte gälten folgende Regeln:
Verwende echtes `null`, kein `"null"` als String!
Verwende keine Anführungszeichen um null. null muss ein JSON-Wert sein, kein String.
Wenn der Wert kein null ist, verwende immer Anführungszeichen.

ein Beispiele:
Nutzeranfrage: "Ich muss in 2h 35 min von Puckholm zum Rieck Museum. Wie komme ich dort hin?"
Deine Antwort in Json-Format:
{
    "start": "Puckholm",
    "dest": "Rieck Museum",
    "dest_aoi": null,
    "date": "today", 
    "time": "now + 2h35m",
    "time_is_departure": True,
    "type_of_transport": null  
}

Für die Ortsangaben "start", "dest" und "dest_aoi" gälten folgende Regeln:

Wenn ein POI (z. B. „ein Café“) zusammen mit einem Ort oder Platz genannt wird (z. B. „am Hapischtsplatz“ oder "in St. Pauli" oder "in der Nähe von"), dann:
   - Setze `"dest"` auf den POI (z. B. "Café")
   - Setze `"dest_aoi"` auf das Gebiet oder den Platz (z. B. "Hapischtsplatz" oder "St. Pauli")
 
Beispiel:
Nutzeranfrage: Zeig mir bitte den nächsten Bus von der Station Messberg zu einem Restaurant in der Nähe vom Hauptbanhof

Antwort:
{
  "start": "Messberg",
  "dest": "Restaurant",
  "dest_aoi": "Hauptbanhof",
  "date": "today",
  "time": "now",
  "time_is_departure": true,
  "type_of_transport": "bus"
}

Wenn ein POI (z.B. "Innenstadt") ohne einen Ort oder Platz genannt wird, dann:
   - Setze `"dest"` auf den POI (z. B. "Innenstadt")
   - Setze `"dest_aoi"` auf null

Beispiel:
Nutzeranfrage: Zeig mir den nächsten Bus zur Innenstadt

Antwort:
{
  "start": null,
  "dest": "Innenstadt",
  "dest_aoi": null,
  "date": "today",
  "time": "now",
  "time_is_departure": true,
  "type_of_transport": "bus"
}

Setze den "start"-Wert nur wenn der Input explizit eine Start-Ortsangabe benennt mit Worten wie "von", "ab", "aus", oder Ähnliches
Wenn keine Starts-Ortsangabe genannt wird, setze "start" auf null.
Leite keine Starts-Ortsangabe vom Ziel ab. 

Tippfehler in Angaben zum Zielort (z. B. "Innenstatt" oder "Inennstadt") sollen nicht korrigiert werden.
Wenn „dest“ ein Ort mit eindeutiger Adresse oder Haltestelle ist (z. B. „Rehkoppel“), dann ist "dest_aoi" = null

Für die Zeitangaben gälten folgende Regeln:
Zeitangaben wie „ca. 15:00“, „ungefähr 18 Uhr“, „etwa 7:30“ sollen als konkrete Zeit interpretiert und im Format "HH:MM" ausgegeben werden – NICHT als "now" oder als Originaltext mit "ca.".

Wenn eine konkrete Uhrzeit genannt wird („ca. 16:30“), gib diese direkt als "HH:MM" zurück. Verwende nicht "now + …".

Zeitangaben wie „morgen“, „übermorgen“, „nächste Woche“ sollen relativ als "today + Nd" oder "today + Nw" angegeben werden:
   - „morgen“ = today + 1d
   - „übermorgen“ = today + 2d
   - „nächste Woche“ = today + 1w

Zeitangaben mit "nachmittags", "abends", "morgens" sind auf 24-Stunden-Format zu normieren:
   - z. B. „2 Uhr nachmittags“ = „14:00“, nicht „02:00“

Zeitangaben wie "in 2 Stunden" müssen konvertiert werden in das Format "now + 2h00m"
Nutze immer 2 Ziffern für Minuten, auch wenn es nur Nullen sind. Nutze "00m", nicht "0m"

Wenn der Nutzer sagt, dass er „um XY dort sein muss“, handelt es sich um eine Ankunftszeit, daher setze "time_is_departure" auf false.
Angaben wie "in 3 Stunden in der Bar sein", "muss um 18:00 da sein", "möchte ankommen um ..." geben eine Ankunftszeit an. Daher muss "time_is_departure" auf false gesetzt werden.

Beispiel:
Nutzeranfrage: "Ich muss morgen um 23 Uhr am Kressenweg sein.Fahre von Siloahweg los, mit dem Bus bitte"

Antwort:
{
  "start": "Siloahweg",
  "dest": "Kressenweg",
  "dest_aoi": null,
  "date": "today + 1d",
  "time": "23:00",
  "time_is_departure": false,
  "type_of_transport": "bus"
}

Für Datumsangaben gälten folgende Regeln:

Für die Angabe von exakten Datumsangaben muss immer das Format TT.MM.YYYY verwendet werden.

23.Dezember 2026 wird angegeben als 23.12.2026

Gib nun die beste Antwort passend zur Nutzeranfrage als Json-Objekt zurück.
Die Rückgabe als Json-Objekt in dem folgenden Format ist dabei sehr wichtig:

{
    "start": [Wert],
    "dest": [Wert],
    "dest_aoi": [Wert],
    "date": [Wert], 
    "time": [Wert],
    "time_is_departure": [Wert],
    "type_of_transport": [Wert] 
}

Nutzeranfrage: Ich brauche nächste woche von der Harvertstraße einen Bus in die Innenstadt. Gib mir die Route dazu.
 """
    output = call_api(prompt, {}, {})
    pprint.pp(output)
    output_json = json.loads(output['output'])
    answer_text = output_json['answer']
    json_match = re.search(r"```json\n(.*?)\n```", answer_text, re.DOTALL)
    inner_json_str = json_match.group(1)
    parsed_data = json.loads(inner_json_str)
    print(parsed_data)
    """
    json_match = re.search(r"```json\n(.*?)\n```", answer_text, re.DOTALL)
    inner_json_str = json_match.group(1)
    data = json.loads(inner_json_str)
    print(data)"""
