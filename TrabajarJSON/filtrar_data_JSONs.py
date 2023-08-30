import json
from pathlib import Path

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


def markAsOldData(i, newFile):
    Path(OldData).mkdir(parents=True, exist_ok=True)
    with open(OldData[i], 'w', encoding='utf-8') as outfile:
        json.dump(newFile, outfile)


def searchEstacionData(code, dataFile):
    for data in dataFile:
        if data['estacion'] == code:
            return data["datos"]

def refineData(index, newFile, oldFile):
    refinedFile = []

    for i, item in enumerate(newFile):
        newData = []
        for data in item["datos"]:
            oldData = searchEstacionData(item['estacion'], oldFile)
            if data["fecha y hora"] not in [x["fecha y hora"] for x in oldData]:
                print(f"Found difference: {data}")
                newData.append(data)
        if newData:
            refinedFile.append(
                {
                    "estacion": item["estacion"],
                    "dato": newData
                }
            )

    saveRefinedData(index, refinedFile)


for i in range(len(ParsedData)):
    with open(ParsedData[i], "r", encoding="utf-8") as f:
        newFile = json.loads(f.read())
    with open(OldData[i], "r", encoding="utf-8") as f:
        oldFile = json.loads(f.read())

    refineData(i, newFile, oldFile)
    markAsOldData(i, newFile)

