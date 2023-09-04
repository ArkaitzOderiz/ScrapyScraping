import json
import sys

import requests

url = "http://localhost:8000/polls/storeData"

for i in sys.argv[1:]:
    with open(f"Scrapy/{i}Spider/JSONs/RefinedData/datos_{i}.json", encoding="utf-8") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)

    with open('response.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
