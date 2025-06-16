import json
import re
from langchain_ollama import ChatOllama
import os
import requests
import logging
import codecs

token = os.getenv("x-api-key")


def raw_llm2json(raw_llm_output):
    try:
        if "answer" in raw_llm_output and "<think>" not in raw_llm_output:
            m = re.findall(r"json.*(\{.*?\})", raw_llm_output, re.DOTALL)
            decoded = codecs.decode(m[0], 'unicode_escape')
            json_output = json.loads(decoded)
        else:
            json_pattern = r'\{[\s\S]*?\}'
            matches = re.findall(json_pattern, raw_llm_output)
            if matches:
                json_str = None
                for candidate in matches:
                    try:
                        json_output = json.loads(candidate)
                        json_str = candidate  # Save the valid one
                        break
                    except json.JSONDecodeError:
                        continue
            
                if json_str is None:
                    print("Error: No valid JSON object found in text")
                    return False

                json_output = json.loads(json_str)
            else:
                return False
            
        # Check if it has the expected structure
        if not isinstance(json_output, dict):
            print("Error: Output is not a dictionary")
            return False
            
        # Check for required fields based on the new prompt format
        required_fields = [
            "start", "dest", "dest_aoi", 
            "date", "time", "time_is_departure", "type_of_transport"
        ]
        
        for field in required_fields:
            if field not in json_output:
                print(f"Error: Missing '{field}' field")
                return False
                
            # Check that fields have appropriate types
            if field in ["start", "dest", "dest_aoi", "date", "time", "type_of_transport"]:
                # These fields should be None or string
                if json_output[field] is not None and not isinstance(json_output[field], str):
                    print(f"Error: Field '{field}' is not None or a string")
                    return False
            elif field == "time_is_departure":
                # time_is_departure should be a boolean
                if not isinstance(json_output[field], bool) and json_output[field] is not None:
                    print(f"Error: Field '{field}' is not a boolean")
                    return False
        return json_output
            
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
def call_gemma3_4b(prompt):
    model = "gemma3:4b"
    model_url = "http://localhost:11434"
    # Initialize Llama model via Ollama
    ollama = ChatOllama(
        model=model,
        base_url=model_url,
        temperature=0
    )
    response = ollama.invoke(prompt)
    
    return  response.content

def call_mistral_7b(prompt):
    model = "mistral:7b"
    model_url = "http://localhost:11434"
    # Initialize Llama model via Ollama
    ollama = ChatOllama(
        model=model,
        base_url=model_url,
        temperature=0
    )
    response = ollama.invoke(prompt)
    
    return  response.content

def call_mistral_small_3_1_24b(prompt):
    model = "mistral-small3.1:latest"
    model_url = "http://localhost:11434"
    # Initialize Llama model via Ollama
    ollama = ChatOllama(
        model=model,
        base_url=model_url,
        temperature=0
    )
    response = ollama.invoke(prompt)
    
    return  response.content

def call_qwen3_4b(prompt):
    model = "qwen3:4b"
    model_url = "http://localhost:11434"
    # Initialize Llama model via Ollama
    ollama = ChatOllama(
        model=model,
        base_url=model_url,
        temperature=0
    )
    response = ollama.invoke(prompt)
    
    return  response.content
    
def call_llama3_3(prompt):
    model = "Llama3.2"
    model_url = "https://bc4ai.api.datis.de/api/chat"
    headers = {
    "Content-Type": "application/json",
    "x-api-key": token,
    "User-Agent": "PostmanRuntime/7.44.0",
    "Accept": "*/*",
    "Cache-Control": "no-cache",
    "Host": "bc4ai.api.datis.de",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    }
    data = {
    "query": prompt,     
    "model": model
    }
    response = requests.post(model_url, headers=headers, json=data)
    
def call_phi_4(prompt):
    model = "phi4:latest"
    model_url = "https://bc4ai.api.datis.de/api/chat"
    headers = {
    "Content-Type": "application/json",
    "x-api-key": token,
    "User-Agent": "PostmanRuntime/7.44.0",
    "Accept": "*/*",
    "Cache-Control": "no-cache",
    "Host": "bc4ai.api.datis.de",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    }
    data = {
    "query": prompt,     
    "model": model
    }
    response = requests.post(model_url, headers=headers, json=data)
    
    return response.text

if __name__ == "__main__":
    #retur = '{"answer":"```json\n{\n  \"start\": null,\n  \"dest\": \"Innenstadt\",\n  \"dest_aoi\": null,\n  \"date\": \"null\",\n  \"time\": \"08:00\",\n  \"time_is_departure\": true,\n  \"type_of_transport\": \"Bus\"\n}\n```\n\nBegründung:\nDie Frage nach dem nächsten Bus in die Innenstadt ist sehr vage. Um eine Antwort zu geben, muss ich davon ausgehen, dass der nächste Bus in der Nähe des aktuellen Standorts abfährt und der Zielort genau identifiziert werden kann. Da keine spezifischen Informationen über den aktuellen Standort oder die genaue Route angegeben wurden, kann ich nur eine allgemeine Antwort geben.\n\nUm die beste Antwort zu geben, müsste ich wissen, wo sich der aktuelle Standort befindet und welche Buslinie in der Nähe verkehrt. Ohne diese Informationen kann ich keine genauere Antwort geben.","context":null,"references":[]}'
    #r = json.loads(retur)
    #json_pattern = r'\{[\s\S]*?\}'
    #matches = re.findall(json_pattern, r["answer"])[0]
    #f = json.loads(matches)
    #f = raw_llm2json(input)
    #print(f)
    pass