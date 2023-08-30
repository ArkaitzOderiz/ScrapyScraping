import json
from pathlib import Path

CodeJSON = "JSONs/RawCode/codigos_aemet.json"


def openFile(filename):
    with open(f'JSONs/RawData/{filename}', "r", encoding="utf-8") as f:
        file = json.loads(f.read())
    return file


def saveFile(filename, data):
    Path("JSONs/ParsedCode").mkdir(parents=True, exist_ok=True)
    with open(f'JSONs/ParsedCode/{filename}', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def searchEstacionCoords(code, coordFile):
    for data in coordFile:
        if data['estacion'] == code:
            return data['coordenadas']


def formatCode(file):
    coordFile = openFile('datos_aemet.json')
    formattedJSON = []
    for line in file:
        lineCoords = searchEstacionCoords(line['codigo'], coordFile)
        header = {
            'estacion': line['estacion'],
            'codigo': line['codigo'],
            'coordenadas': lineCoords,
            'seguimiento': None,
            'prealerta': None,
            'alerta': None,

        }
        formattedJSON.append(header)
    saveFile('codigos_aemet.json', formattedJSON)


def main():
    with open(CodeJSON, "r", encoding="utf-8") as f:
        file = json.loads(f.read())

    formatCode(file)


if __name__ == "__main__":
    main()
