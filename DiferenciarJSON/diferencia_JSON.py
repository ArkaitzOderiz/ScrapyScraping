import json

with open("datos_aemet1.json", "r") as f1:
    file1 = json.loads(f1.read())
with open("datos_aemet2.json", "r") as f2:
    file2 = json.loads(f2.read())

file3 = []

for i, item in enumerate(file1):
    repeat = []
    for data in item["datos"]:
        if data["hora"] not in [x["hora"] for x in file2[i]["datos"]]:
            print(f"Found difference: {data}")
            repeat.append(data)
    if repeat:
        file3.append({
            "municipio": item["municipio"],
            "dato": repeat})

print(file3)