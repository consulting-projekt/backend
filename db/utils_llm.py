import json
import re
from langchain_ollama import ChatOllama

def raw_llm2json(raw_llm_output):
    try:
        # Check if the text contains markdown code block
        json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        matches = re.findall(json_pattern, raw_llm_output)
        
        if matches:
            # Use the first JSON code block found
            json_str = matches[0].strip()
            json_output = json.loads(json_str)
        else:
            # Try parsing the entire text as JSON
            json_output = json.loads(raw_llm_output)
        
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
    model_url = "http://localhost:11435"
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
    model_url = "http://localhost:11436"
    # Initialize Llama model via Ollama
    ollama = ChatOllama(
        model=model,
        base_url=model_url,
        temperature=0
    )
    response = ollama.invoke(prompt)
    
    return  response.content