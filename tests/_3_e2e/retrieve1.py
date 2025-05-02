from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from tests._1_params_extract.retrieve_gemma3_4b import call_api as call_api_gemma3_4b
from db.utils_llm import raw_llm2json
from db.utils_qdrant import get_startdest_std, get_point_std
from db.utils_geofox import get_route_params, get_route
from qdrant_client import QdrantClient
from db.geofox_client import get_geofox_client
from db.utils_llm import call_gemma3_4b
from db.utils_data import find_point

client_qdrant = QdrantClient("localhost", port=6333)
client_geofox = get_geofox_client()
MIN_EMBEDDING_SCORE = 0.55

def call_api(prompt, options, context):
    anfrage = context.get('vars', {}).get('anfrage', '')
    params_extract_res = call_gemma3_4b(prompt)
    params_json = raw_llm2json(params_extract_res)
    
    problems = []
    
    # resultierende dict werte mit defaults belegen
    # falls für start und dest in cases.py keine defaults hinterlegt sind (unter "vars") dann ist das ein simuliertes Problem
    start = params_json.get("start")
    start = context.get('vars', {}).get('start', start) if start is None else start
    dest = params_json.get("dest")
    dest = context.get('vars', {}).get('dest', dest) if dest is None else dest
    dest_aoi = params_json.get("dest_aoi")
    date = params_json.get("date")
    date = context.get('vars', {}).get('date', date) if date is None else date
    time = params_json.get("time")
    time = context.get('vars', {}).get('time', time) if time is None else time
    time_is_departure = params_json.get("time_is_departure", True)
    type_of_transport = params_json.get("type_of_transport", None)
        
    if start is None:
        problems.append("Es wurde kein Startpunkt angegeben.")
    if dest is None:
        problems.append("Es wurde kein Zielpunkt angegeben.")
        
    if len(problems) > 0:
        # Read the prompt template from file
        prompt = get_problems_prompt(anfrage, params_json, problems)
        
        return {
            "output": call_gemma3_4b(prompt)
        } 
        
    start_with_coordinates = find_point(start)
    dest_with_coordinates = find_point(dest)
    if start_with_coordinates is None:
        start_with_coordinates = get_point_std(client_qdrant, start, None)
        if start_with_coordinates['score'] < MIN_EMBEDDING_SCORE:
            start_with_coordinates = None
    if dest_with_coordinates is None:
        dest_with_coordinates = get_point_std(client_qdrant, dest, dest_aoi)
        if dest_with_coordinates['score'] < MIN_EMBEDDING_SCORE:
            dest_with_coordinates = None
        
    if start_with_coordinates is None:
        problems.append(f"Der Startpunkt '{start}' konnte nicht gefunden werden.")
    if dest_with_coordinates is None:
        problems.append(f"Der Zielpunkt '{dest}' konnte nicht gefunden werden.")
        
    if len(problems) > 0:
        # Read the prompt template from file
        prompt = get_problems_prompt(anfrage, params_json, problems)
        
        return {
            "output": call_gemma3_4b(prompt)
        }     
       
    start_param, dest_param, time_param, penalties_param, time_is_departure = get_route_params(start_with_coordinates, dest_with_coordinates, date, time, time_is_departure, type_of_transport)
    route = get_route(client_geofox, start_param, dest_param, time_param, penalties_param, time_is_departure)[0]
    route2 = {"start": route['start'], "dest": route['dest'], "departure": route['realDepartureTime'], "arrival": route['realArrivalTime']}
    

    # Read the prompt template from file
    prompt = get_route_prompt(anfrage, params_json, route2)
    
    return {
        "output": call_gemma3_4b(prompt),
    }  
    
def get_route_prompt(anfrage, params_json, route_infos):
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
    formatted_prompt = formatted_prompt.replace("{{api_result}}", str(route_infos))   
    return formatted_prompt
    
def get_problems_prompt(anfrage, params_json, problems):
    # Read the prompt template from file
    try:
        with open(Path(__file__).parent / "prompt_step2_with_problems.txt", "r", encoding="utf-8") as file:
            prompt_template = file.read()
    except Exception as e:
        print(f"Error reading prompt.txt: {e}")
        prompt_template = "Error reading template file"
    
    # Replace placeholders with actual values
    formatted_prompt = prompt_template
    formatted_prompt = formatted_prompt.replace("{{anfrage}}", anfrage)
    formatted_prompt = formatted_prompt.replace("{{params_extracted}}", str(params_json))
    formatted_prompt = formatted_prompt.replace("{{problems}}", str(problems))   
    return formatted_prompt
    
    



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

Nutzeranfrage: Wann kommt der nächste Bus in die Innenstadt?
            """
    call_api(prompt, {}, {"vars": {        "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 

            "start": "Lutterothstraße",
            
            "dest": "Innenstadt",
            "dest_aoi": None,
            "date": "today", 
            "time": "now",
            "time_is_departure": True,
            "type_of_transport": "bus"}})
