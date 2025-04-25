import os
import ollama
from langchain_ollama import ChatOllama

model = "gemma3:4b"
model_url = "http://localhost:11434"

def call_api(prompt, options, context):
    # Initialize Llama model via Ollama
    ollama = ChatOllama(
        model=model,
        base_url=model_url,
        temperature=0
    )
    response = ollama.invoke(prompt)
    
    return {
        "output": response.content,
    }




if __name__ == "__main__":
    # Example usage
    prompt = """
Du bist ein experte im öffentlichen Nahverkehr und hast die Aufgabe basierend auf einer Nutzeranfrage folgende entities zu extrahieren:

"start": mögliche Werte= null, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
"start_aoi":  mögliche Werte= null, <start aoi> wenn für "start" adresse|station|poi angegeben
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
    "start_aoi": null,
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