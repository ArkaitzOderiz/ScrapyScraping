import json
from pathlib import Path

OldDir = "JSONs/OldData/"
ParsedDir = "JSONs/ParsedData/"
RefinedDir = "JSONs/RefinedData/"
DataJSON = "datos_meteoNavarra.json"


def openFile(fileDir):
    try:
        with open(fileDir + DataJSON, "r", encoding="utf-8") as f:
            file = json.loads(f.read())
    except FileNotFoundError:
        file = None
    return file


def saveData(jsonDir, DataFile):
    Path(jsonDir).mkdir(parents=True, exist_ok=True)
    with open(jsonDir + DataJSON, 'w', encoding='utf-8') as outfile:
        json.dump(DataFile, outfile)


def searchEstacionData(code, dataFile):
    for data in dataFile:
        if data['estacion'] == code:
            return data["datos"]


def refineData(newFile, oldFile):
    refinedFile = []

    for i, item in enumerate(newFile):
        newData = []
        for data in item["datos"]:
            oldData = searchEstacionData(item['estacion'], oldFile)
            if data["fecha y hora"] not in [x["fecha y hora"] for x in oldData]:
                newData.append(data)
        if newData:
            refinedFile.append(
                {
                    "estacion": item["estacion"],
                    "datos": newData
                }
            )

    saveData(RefinedDir, refinedFile)


def main():
    newFile = openFile(ParsedDir)
    oldFile = openFile(OldDir)

    if oldFile is None:
        saveData(RefinedDir, newFile)
        saveData(OldDir, newFile)
        return

    refineData(newFile, oldFile)
    saveData(OldDir, newFile)


if __name__ == "__main__":
    main()
