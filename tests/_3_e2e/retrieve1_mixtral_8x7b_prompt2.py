from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402
from db.utils_data import find_point
from db.utils_llm import call_mixtral_8x7b, call_gemma3_4b
from db.geofox_client import get_geofox_client
from qdrant_client import QdrantClient
from db.utils_geofox import get_route_params2, get_route, get_route_params1
from db.utils_qdrant_3_e2e import get_point_std
from db.utils_llm import raw_llm2json
from datetime import datetime


client_qdrant = QdrantClient("localhost", port=6333)
client_geofox = get_geofox_client()
MIN_SIMILARITY_SCORE_DEST = 0.5
MIN_SIMILARITY_SCORE_START = 0.5


def call_api(prompt, options, context):
    anfrage = context.get('vars', {}).get('anfrage', '')
    params_extract_res = call_gemma3_4b(prompt)
    params_json = raw_llm2json(params_extract_res)

    problems = []

    # resultierende dict werte mit defaults belegen
    # falls für start und dest in cases.py keine defaults hinterlegt sind (unter "vars") dann ist das ein simuliertes Problem
    try:
        start = params_json.get("start")
    except:
        start = None
    start = context.get('vars', {}).get(
        'start', start) if start is None else start
    try:
        date = params_json.get("date")
    except:
        date = None
    try:
        time = params_json.get("time")
    except:
        time = None
    try:
        dest = params_json.get("dest")
    except:
        dest = None
    try:
        dest_aoi = params_json.get("dest_aoi")
    except:
        dest_aoi = None
    try:
        time_is_departure = params_json.get("time_is_departure", True)
    except:
        time_is_departure  = None
    try:
        type_of_transport = params_json.get("type_of_transport", None)
    except:
        type_of_transport  = None

    if start is None:
        problems.append("Es wurde kein Startpunkt angegeben.")
    if dest is None:
        problems.append("Es wurde kein Zielpunkt angegeben.")

    time_param = get_route_params1(date, time)

    if len(problems) > 0:
        # Read the prompt template from file
        prompt = get_problems_prompt(anfrage, params_json, problems)

        return {
            "output": {
                "answer": call_mixtral_8x7b(prompt),
                "vars": {
                    "start": start,
                    "dest": dest,
                    "date": time_param['date'],
                    "time": time_param['time'],
                }
            }
        }

    start_with_coordinates = find_point(start)
    dest_with_coordinates = find_point(dest)
    if start_with_coordinates is None:
        start_with_coordinates = get_point_std(client_qdrant, start, None)
        if start_with_coordinates['score'] < MIN_SIMILARITY_SCORE_START:
            start_with_coordinates = None
    if dest_with_coordinates is None:
        dest_aoi_location = find_point(dest_aoi)
        dest_aoi_location = dest_aoi_location['location'] if dest_aoi_location else None
        dest_with_coordinates = get_point_std(
            client_qdrant, dest, dest_aoi, point_condition_location=dest_aoi_location)
        if dest_with_coordinates['score'] < MIN_SIMILARITY_SCORE_DEST:
            dest_with_coordinates = None

    if start_with_coordinates is None:
        problems.append(
            f"Der Startpunkt '{start}' konnte nicht gefunden werden.")
    if dest_with_coordinates is None:
        problems.append(
            f"Der Zielpunkt '{dest}' konnte nicht gefunden werden.")

    if len(problems) > 0:
        # Read the prompt template from file
        prompt = get_problems_prompt(anfrage, params_json, problems)

        return {
            "output": {
                "answer": call_mixtral_8x7b(prompt),
                "vars": {
                    "start": start,
                    "dest": dest,
                    "date": time_param['date'],
                    "time": time_param['time'],
                }
            }
        }

    start_param, dest_param, penalties_param, time_is_departure = get_route_params2(
        start_with_coordinates, dest_with_coordinates, time_is_departure, type_of_transport)
    route = get_route(client_geofox, start_param, dest_param,
                      time_param, penalties_param, time_is_departure)[0]

    # Parse the date string into a datetime object (ignoring the timezone offset)
    dt_dep = datetime.strptime(route['realDepartureTime']
                               [:-5], '%Y-%m-%dT%H:%M:%S.%f')
    # Format the time as HH:MM
    formatted_dep_time = dt_dep.strftime('%H:%M')
    formatted_dep_date = dt_dep.strftime('%d.%m.%Y')

    # Parse the date string into a datetime object (ignoring the timezone offset)
    dt_arrival = datetime.strptime(route['realArrivalTime']
                                   [:-5], '%Y-%m-%dT%H:%M:%S.%f')
    # Format the time as HH:MM
    formatted_arrival_time = dt_arrival.strftime('%H:%M')
    formatted_arrival_date = dt_arrival.strftime('%d.%m.%Y')

    route2 = {"start": route['start']['name'], "dest": route['dest']['name'],
              "departure_date": formatted_dep_date, "departure_time": formatted_dep_time, "arrival_time": formatted_arrival_time, "arrival_date": formatted_arrival_date}

    # Read the prompt template from file
    prompt = get_route_prompt(anfrage, params_json, route2)

    return {
        "output": {
            "answer": call_mixtral_8x7b(prompt),
            "vars": {
                "start": route['start']['name'],
                "dest": route['dest']['name'],
                "date": formatted_dep_date,
                "time": formatted_dep_time,
            }
        }
    }


def get_route_prompt(anfrage, params_json, route_infos):
    # Read the prompt template from file
    try:
        with open(Path(__file__).parent / "prompt_step2_v2.txt", "r", encoding="utf-8") as file:
            prompt_template = file.read()
    except Exception as e:
        print(f"Error reading prompt.txt: {e}")
        prompt_template = "Error reading template file"

    # Replace placeholders with actual values
    formatted_prompt = prompt_template
    formatted_prompt = formatted_prompt.replace("{{anfrage}}", anfrage)
    formatted_prompt = formatted_prompt.replace(
        "{{params_extracted}}", str(params_json))
    formatted_prompt = formatted_prompt.replace(
        "{{api_result}}", str(route_infos))
    return formatted_prompt


def get_problems_prompt(anfrage, params_json, problems):
    # Read the prompt template from file
    try:
        with open(Path(__file__).parent / "prompt_step2_with_problems_v2.txt", "r", encoding="utf-8") as file:
            prompt_template = file.read()
    except Exception as e:
        print(f"Error reading prompt.txt: {e}")
        prompt_template = "Error reading template file"

    # Replace placeholders with actual values
    formatted_prompt = prompt_template
    formatted_prompt = formatted_prompt.replace("{{anfrage}}", anfrage)
    formatted_prompt = formatted_prompt.replace(
        "{{params_extracted}}", str(params_json))
    formatted_prompt = formatted_prompt.replace("{{problems}}", str(problems))
    return formatted_prompt


if __name__ == "__main__":
    # Example usage
    prompt = """
Du bist ein experte im öffentlichen Nahverkehr und hast die Aufgabe basierend auf einer Nutzeranfrage folgende entities zu extrahieren:

"start": mögliche Werte= null, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
"dest":  mögliche Werte= null, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
"dest_aoi":  mögliche Werte= null, <dest aoi> wenn für "dest" adresse|station|poi angegeben
"date":  mögliche Werte= null, today, today + 4d7w3m (d:Tage, w:Wochen, m:monate) Datum mit Zielformat: 22.04.2025
"time": mögliche Werte= null, now, now + 2m3h (m:Minuten, h:Stunden) Zeit mit Zielformat: 18:30
"time_is_departure":  mögliche Werte= true, false; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
"type_of_transport":  mögliche Werte= null, bus, train


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

Gib nun die beste Antwort passend zur Nutzeranfrage zurück.

Nutzeranfrage: Ich benötge in 2h und 30 min ein bus vom Hochrad zu einem Einkaufszentrum in der Nähe des Windmühlenweg
            """
    call_api(prompt, {}, {"vars": {"anfrage": "Ich benötge in 2h und 30 min ein bus vom Hochrad zu einem Einkaufszentrum in der Nähe des Windmühlenweg",

                                   "start": None,
                                   "date": None,
                                   "time": None,
                                   }})
