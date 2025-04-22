import os
from langchain_community.llms import Ollama
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
    
    # Evaluate response

    
    return {
        "output": response.content,
    }



if __name__ == "__main__":
    # Example usage
    prompt = """
            hallo
            """
    call_api(prompt, {}, {})