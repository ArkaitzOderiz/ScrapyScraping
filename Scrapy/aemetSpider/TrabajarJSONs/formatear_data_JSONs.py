import json
from datetime import datetime
from pathlib import Path

DataJSON = "datos_aemet.json"


def openFile(filename):
    with open(f'JSONs/RawData/{filename}', "r", encoding="utf-8") as f:
        file = json.loads(f.read())
    return file


def saveFile(filename, data):
    Path("JSONs/ParsedData").mkdir(parents=True, exist_ok=True)
    with open(f'JSONs/ParsedData/{filename}', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def formatData(file):
    formattedJSON = []
    for line in file:
        datos = []
        for data in line['datos']:
            dato = {
                'fecha y hora': datetime.strptime(data['fecha y hora'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M"),
                'temperatura (ºC)': data['temperatura (ºC)'],
                'humedad (%)': data['humedad (%)'],
                'precipitacion (mm)': data['precipitacion (mm)'],
                'nivel (m)': None,
                'caudal (m^3/s)': None,
                'radiacion (W/m^2)': None,
            }
            datos.append(dato)
        header = {
            'coordenadas': line['coordenadas'],
            'estacion': line['estacion'],
            'datos': datos
        }
        formattedJSON.append(header)
    saveFile(DataJSON, formattedJSON)


def main():
    file = openFile(DataJSON)
    formatData(file)


if __name__ == "__main__":
    main()
