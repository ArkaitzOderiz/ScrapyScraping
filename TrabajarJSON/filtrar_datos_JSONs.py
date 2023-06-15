import json
from datetime import date, datetime

OldData = [
    "../JSONs/OldData/old_datos_aemet.json",
    "../JSONs/OldData/old_datos_aguaEnNavarra.json",
    "../JSONs/OldData/old_datos_chcantabrico.json",
    "../JSONs/OldData/old_datos_meteoNavarra.json",
]

ParsedData = [
    "../JSONs/ParsedData/datos_aemet.json",
    "../JSONs/ParsedData/datos_aguaEnNavarra.json",
    "../JSONs/ParsedData/datos_chcantabrico.json",
    "../JSONs/ParsedData/datos_meteoNavarra.json",
]

RefinedData = [
    "../JSONs/RefinedData/datos_aemet.json",
    "../JSONs/RefinedData/datos_aguaEnNavarra.json",
    "../JSONs/RefinedData/datos_chcantabrico.json",
    "../JSONs/RefinedData/datos_meteoNavarra.json",
]


def saveRefinedData(i, refinedFile):
    with open(RefinedData[i], 'w', encoding='utf-8') as outfile:
        json.dump(refinedFile, outfile)


def refineData(index, newFile, oldFile):
    refinedFile = []
    fechaActual = date.today().strftime("%d/%m/%Y")

    for i, item in enumerate(newFile):
        newData = []
        for data in item["datos"]:
            if data["fecha y hora"] not in [x["fecha y hora"] for x in oldFile[i]["datos"]]:
                print(f"Found difference: {data}")
                fechaDato = datetime.strptime(data["fecha y hora"], "%d/%m/%Y %H:%M:%S").date().strftime("%d/%m/%Y")
                if fechaActual == fechaDato:
                    newData.append(data)
        if newData:
            refinedFile.append(
                {
                    "coordenadas": item["coordenadas"],
                    "estacion": item["estacion"],
                    "dato": newData
                }
            )

    saveRefinedData(index, refinedFile)


def markAsOldData(i, newFile):
    with open(OldData[i], 'w', encoding='utf-8') as outfile:
        json.dump(newFile, outfile)


for i in range(len(ParsedData)):
    with open(ParsedData[i], "r", encoding="utf-8") as f:
        newFile = json.loads(f.read())
    with open(OldData[i], "r", encoding="utf-8") as f:
        oldFile = json.loads(f.read())

    refineData(i, newFile, oldFile)
    markAsOldData(i, newFile)

