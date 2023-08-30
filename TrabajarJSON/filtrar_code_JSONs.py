import json
from pathlib import Path

OldCode = [
    "../JSONs/OldCode/old_codigos_aemet.json",
    "../JSONs/OldCode/old_codigos_aguaEnNavarra.json",
    "../JSONs/OldCode/old_codigos_chcantabrico.json",
    "../JSONs/OldCode/old_codigos_meteoNavarra.json",
]

ParsedCode = [
    "../JSONs/ParsedCode/codigos_aemet.json",
    "../JSONs/ParsedCode/codigos_aguaEnNavarra.json",
    "../JSONs/ParsedCode/codigos_chcantabrico.json",
    "../JSONs/ParsedCode/codigos_meteoNavarra.json",
]

RefinedCode = [
    "../JSONs/RefinedCode/codigos_aemet.json",
    "../JSONs/RefinedCode/codigos_aguaEnNavarra.json",
    "../JSONs/RefinedCode/codigos_chcantabrico.json",
    "../JSONs/RefinedCode/codigos_meteoNavarra.json",
]


def saveRefinedCode(i, refinedFile):
    with open(RefinedCode[i], 'w', encoding='utf-8') as outfile:
        json.dump(refinedFile, outfile)


def markAsOldCode(i, newFile):
    Path(OldCode).mkdir(parents=True, exist_ok=True)
    with open(OldCode[i], 'w', encoding='utf-8') as outfile:
        json.dump(newFile, outfile)


def searchEstacionData(code, dataFile):
    for data in dataFile:
        if data['estacion'] == code:
            return data["datos"]


def refineCode(index, newFile, oldFile):
    refinedFile = []

    for item in newFile:
        newCode = []
        if item["codigo"] not in [x["codigo"] for x in oldFile]:
            print(f"Found difference: {item}")
            newCode.append(item)

    saveRefinedCode(index, refinedFile)


for i in range(len(ParsedCode)):
    with open(ParsedCode[i], "r", encoding="utf-8") as f:
        newFile = json.loads(f.read())
    with open(OldCode[i], "r", encoding="utf-8") as f:
        oldFile = json.loads(f.read())

    refineCode(i, newFile, oldFile)
    markAsOldCode(i, newFile)

