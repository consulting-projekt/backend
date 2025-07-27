#import tests._3_e2e.retrieve1_llama3_3_api_prompt2 as yo
#import tests._3_e2e.retrieve1_gemma3_4b_prompt2 as yo

#prompt = """
#        Du bist ein experte im öffentlichen Nahverkehr und hast die Aufgabe basierend auf einer Nutzeranfrage folgende entities zu extrahieren:
#
#        "start": mögliche Werte= null, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
#        "dest":  mögliche Werte= null, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
#        "dest_aoi":  mögliche Werte= null, <dest aoi> wenn für "dest" adresse|station|poi angegeben
#        "date":  mögliche Werte= null, today, today + 4d7w3m (d:Tage, w:Wochen, m:monate) Datum mit Zielformat: 22.04.2025
#        "time": mögliche Werte= null, now, now + 2m3h (m:Minuten, h:Stunden) Zeit mit Zielformat: 18:30
#        "time_is_departure":  mögliche Werte= true, false; wenn true dann ist die Zeit eine Abfahrtszeit, wenn false dann ist es eine Ankunftszeit
#        "type_of_transport":  mögliche Werte= null, bus, train
#
#
#        ein Beispiele:
#        Nutzeranfrage: "Ich muss in 2h 35 min von Puckholm zum Rieck Museum. Wie komme ich dort hin?"
#        Deine Antwort in Json-Format:
#        {
#            "start": "Puckholm",
#            "dest": "Rieck Museum",
#            "dest_aoi": null,
#            "date": "today", 
#            "time": "now + 2h35m",
#            "time_is_departure": True,
#            "type_of_transport": null  
#        }
#
#        Gib nun die beste Antwort passend zur Nutzeranfrage zurück.
#
#        Nutzeranfrage: Ich benötge in 2h und 30 min ein bus vom Hochrad zu einem Einkaufszentrum in der Nähe des Windmühlenweg
#    """
#options = {}

#context = {"vars": {"anfrage": "Ich brauche um ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
#                    # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
#                    "start": None,
#                    "answer": "Von wo möchtest du starten? Dann berechnen wir dir gerne die Route nach <DEST> um <TIME>." 
#                    #"answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen dir eine angenehme Fahrt!"
#                    }}


#print(yo.call_api(prompt, options, context))

import src.utils_llm as llm
import json
import re

prompt = '''
        Du bist ein experte im öffentlichen Nahverkehr und hast die Aufgabe Reisenden bei der Routenplanung zu helfen.

        Nutzeranfrage: 
        "Ich brauche um ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu."

        Extrahierte Parameter: 
        "start": null,
        "dest": "Innenstadt",
        "date": "18.06.2025",
        "time": "16:06"

        Erkannte Probleme:
        Es wurde kein Startpunkt angegeben.

        Bitte stelle dem Nutzer Rückfragen um die Probleme zu lösen. Nutze hierfür das höfliche "du". Formuliere deine Rückfragen so knapp, wie möglich und so lang, wie nötig. 
        Wichtig: Nutze auf keinen Fall "Hallo", "Hallo!", "Moin", "Alles klar" und ähnliche Begrüßungen zu Beginn deiner Antwort. Starte stattdessen direkt mit der Route bzw. deiner Antwort! Kein Hallo am Satzanfang nutzen!


        Beispiel:
        """
        Beispiel-Kundenanfrage: Ich möchte die schnellste Route zum Hafen.
        Musterantwort: Von wo möchtest du starten? Dann berechnen wir dir gerne die Route zum Hafen.
        """

        '''

prompt_2_extract =  '''
                    Du bist ein experte im öffentlichen Nahverkehr und hast die Aufgabe basierend auf einer Nutzeranfrage folgende entities zu extrahieren:

                    "start": mögliche Werte= null, <start adresse|station|poi>, <start aoi> wenn keine adresse|station|poi angegeben
                    "dest":  mögliche Werte= null, <dest adresse|station|poi>, <dest aoi> wenn keine adresse|station|poi angegeben
                    "dest_aoi":  mögliche Werte= null, <dest aoi> wenn für "dest" adresse|station|poi angegeben
                    "date":  mögliche Werte= null, today, today + 3m3w5d (d:Tage, w:Wochen, m:monate), Datum mit Zielformat: 22.04.2025
                    "time": mögliche Werte= null, now, now + 3h2m (m:Minuten, h:Stunden), Zeit mit Zielformat: 18:30
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

                    Gib nun die beste Antwort passend zur Nutzeranfrage als Json-Objekt zurück.

                    Nutzeranfrage: "Ich brauche um ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu."
                    '''
#llm_return = llm.call_llama3_3(prompt_2_extract)
#j = json.loads(llm_return)
#print(j['answer'])

#llm_return = llm.call_mixtral_8x7b(prompt)
#j = json.loads(llm_return)
#print(j['answer'])

print(re.sub(r"<think>.*?</think>.{2}", "", llm.call_qwen3_4b(prompt), flags=re.DOTALL))
