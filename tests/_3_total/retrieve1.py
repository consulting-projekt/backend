import os
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from tests._1_params_extract.retrieve_gemma3_4b import call_api as call_api_gemma3_4b
from db.utils_llm import raw_llm2json
from db.utils_qdrant import get_startdest_std
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

def call_api(prompt, options, context):
    params_extract_res = call_api_gemma3_4b(prompt, options, context)["output"]
    params_json = raw_llm2json(params_extract_res)
    start, dest = get_startdest_std(client, params_json)

