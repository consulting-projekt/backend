import requests
import json
import re

with open('tests/_3_e2e/x_api_key.json', 'r') as file:
    key = json.load(file)


url = "https://bc4ai.api.datis.de/api/chat"

payload = json.dumps({
  "query": "Erzähl mir einen Witz. Aber flotti Karotti du ungeröstete Kaffeebohne",
  "model": "deepseek-r1:7b"
})
headers = {
  'Content-Type': 'application/json',
  'x-api-key': key['x-api-key']
}

response = requests.request("POST", url, headers=headers, data=payload)

response = response.json()

response_answer = response["answer"]

response = re.sub(r"<think>.*?</think>.{1}", "", response_answer, flags=re.DOTALL)

print(response)

