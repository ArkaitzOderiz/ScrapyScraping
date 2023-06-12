import json
from datetime import date, datetime

with open("datos_aemet1.json", "r", encoding="utf-8") as f1:
    file1 = json.loads(f1.read())
with open("datos_aemet2.json", "r", encoding="utf-8") as f2:
    file2 = json.loads(f2.read())

file3 = []

fechaActual = date.today().strftime("%d/%m/%Y")

for i, item in enumerate(file1):
    repeat = []
    for data in item["datos"]:
        if data["fecha y hora"] not in [x["fecha y hora"] for x in file2[i]["datos"]]:
            print(f"Found difference: {data}")
            fechaDato = datetime.strptime(data["fecha y hora"], "%d/%m/%Y %H:%M:%S").date().strftime("%d/%m/%Y")
            if fechaActual == fechaDato:
                repeat.append(data)
    if repeat:
        file3.append({
            "coordenadas": item["coordenadas"],
            "estacion": item["estacion"],
            "dato": repeat})

print(file3)