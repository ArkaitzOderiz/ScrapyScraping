import json
import sys

import requests

url = "http://localhost:8000/polls/storeCode"

with open(f"JSONs/RawCode/codigos_{sys.argv[1]}.json", encoding="utf-8") as f:
    data = json.load(f)
headers = {'content-type': 'application/json'}
r = requests.post(url, json=data, headers=headers)

with open('response.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
