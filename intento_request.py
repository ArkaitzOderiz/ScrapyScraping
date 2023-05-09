import requests

url = "http://localhost:8000/polls/store"
data = {'data': [{'key1': 'val1'}, {'key2': 'val2'}]}
headers = {'content-type': 'application/json'}
r = requests.post(url, json=data, headers=headers)
#print(r.text)

with open('response.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
