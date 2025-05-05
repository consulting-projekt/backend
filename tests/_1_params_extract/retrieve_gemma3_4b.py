from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402

from db.utils_llm import call_gemma3_4b


def call_api(prompt, options, context):
    return {
        "output": call_gemma3_4b(prompt),
    }


if __name__ == "__main__":
    # Example usage
    prompt = """
Du bist ein experte im öffentlichen Nahverkehr und hast die Aufgabe basierend auf einer Nutzeranfrage folgende entities zu extrahieren:

"start": mögliche Werte= null, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
"dest":  mögliche Werte= null, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
"dest_aoi":  mögliche Werte= null, <dest aoi> wenn für "dest" adresse|station|poi angegeben
"date":  mögliche Werte= null, today, today + d|w (d:Tage, w:Wochen) Datum mit Zielformat: 22.04.2025
"time": mögliche Werte= null, now, now + m|h (m:Minuten, h:Stunden) Zeit mit Zielformat: 18:30
"time_is_departure":  mögliche Werte= true, false; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
"type_of_transport":  mögliche Werte= null, bus, train


ein Beispiele:
Nutzeranfrage: "Wann kommt der nächste Bus in die Innenstadt?"
Deine Antwort in Json-Format:
{
    "start": null,
    "dest": "Innenstadt",
    "dest_aoi": null,
    "date": "today", 
    "time": "now",
    "time_is_departure": true,
    "type_of_transport": "bus"
}

Gib nun die beste Antwort passend zur Nutzeranfrage zurück.

Nutzeranfrage: Ich brauche nächste woche von der Harverdstraße einen Bus in die Innenstadt. Gib mir die Route dazu.
            """
    call_api(prompt, {}, {})
