import json
from pathlib import Path

CodeJSON = "codigos_aguaEnNavarra.json"


def openFile(filename):
    with open(f'JSONs/RawCode/{filename}', "r", encoding="utf-8") as f:
        file = json.loads(f.read())
    return file


def saveFile(filename, data):
    Path("JSONs/ParsedCode").mkdir(parents=True, exist_ok=True)
    with open(f'../JSONs/ParsedCode/{filename}', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def formatCode(file):
    formattedJSON = []
    for line in file:
        header = {
            'estacion': line['descripcion'],
            'codigo': line['estacion'],
            'coordenadas': line['coordenadas'],
            'seguimiento': None,
            'prealerta': None,
            'alerta': None,

        }
        formattedJSON.append(header)
    saveFile('codigos_aguaEnNavarra.json', formattedJSON)


def main():
    file = openFile(CodeJSON)
    formatCode(file)


if __name__ == "__main__":
    main()
