from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from tests._1_params_extract.retrieve_gemma3_4b import call_api as call_api_gemma3_4b
from db.utils_llm import raw_llm2json
from db.utils_qdrant import get_startdest_std
from db.utils_geofox import get_route_params, get_route
from qdrant_client import QdrantClient
from db.geofox_client import get_geofox_client
from db.utils_llm import call_gemma3_4b

client_qdrant = QdrantClient("localhost", port=6333)
client_geofox = get_geofox_client()

def call_api(prompt, options, context):
    params_extract_res = call_gemma3_4b(prompt)
    params_json = raw_llm2json(params_extract_res)
    if params_json['start'] is None:
        params_json['start'] = context.get('vars', {}).get('start', 'Herthastraße 1, Hamburg')
    start, dest = get_startdest_std(client_qdrant, params_json)
    start_param, dest_param, time_param, penalties_param, time_is_departure = get_route_params(start, dest, params_json)
    route = get_route(client_geofox, start_param, dest_param, time_param, penalties_param, time_is_departure)[0]
    route2 = {"start": route['start'], "dest": route['dest'], "departure": route['realDepartureTime'], "arrival": route['realArrivalTime']}
    anfrage = context.get('vars', {}).get('anfrage', {})

    # Read the prompt template from file
    try:
        with open(Path(__file__).parent / "prompt_step2.txt", "r", encoding="utf-8") as file:
            prompt_template = file.read()
    except Exception as e:
        print(f"Error reading prompt.txt: {e}")
        prompt_template = "Error reading template file"
    
    # Replace placeholders with actual values
    formatted_prompt = prompt_template
    formatted_prompt = formatted_prompt.replace("{{anfrage}}", anfrage)
    formatted_prompt = formatted_prompt.replace("{{params_extracted}}", str(params_json))
    formatted_prompt = formatted_prompt.replace("{{api_result}}", str(route2))

    
    return {
        "output": call_gemma3_4b(formatted_prompt),
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
    call_api(prompt, {}, {"vars": {"anfrage": "Wann kommt der nächste Bus in die Innenstadt?"}})
