import json

import requests

url = "http://localhost:8000/polls/store"

with open("JSONs/ParsedData/datos_aguaEnNavarra.json", encoding="utf-8") as f:
    data = json.load(f)
headers = {'content-type': 'application/json'}
r = requests.post(url, json=data, headers=headers)
#print(r.text)

with open('response.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
