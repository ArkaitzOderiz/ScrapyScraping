import json
import sys

import requests

url = "http://localhost:8000/polls/storeData"

for i in sys.argv[1:]:
    with open(f"Scrapy/{sys.argv[i]}Spider/JSONs/RefinedData/datos_{sys.argv[i]}.json", encoding="utf-8") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)

    with open('response.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
