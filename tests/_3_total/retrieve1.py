import os
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from tests._1_params_extract.retrieve_gemma3_4b import call_api as call_api_gemma3_4b

model = "qwen2.5:3b"
model_url = "http://localhost:11434"

def call_api(prompt, options, context):
    params_extract_res = call_api_gemma3_4b(prompt, options, context)["output"]
    
