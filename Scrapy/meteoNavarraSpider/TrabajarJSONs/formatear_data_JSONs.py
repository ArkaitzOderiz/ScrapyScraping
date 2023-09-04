import json
from datetime import datetime
from pathlib import Path

DataJSON = "datos_meteoNavarra.json"


def openFile(filename):
    with open(f'JSONs/RawData/{filename}', "r", encoding="utf-8") as f:
        file = json.loads(f.read())
    return file


def saveFile(filename, data):
    Path("JSONs/ParsedData").mkdir(parents=True, exist_ok=True)
    with open(f'JSONs/ParsedData/{filename}', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def searchEstacionCoords(code, coordFile):
    for data in coordFile:
        if data['estacion'] == code:
            return data['coordenadas']


def unifyData(dataFile, cod):
    datos = []
    for line in dataFile:
        if line['estacion'] == cod:
            for dato in line['datos']:
                datos.append(dato)

    unifiedData = {
        'estacion': cod,
        'datos': datos
    }
    return unifiedData


def formatData(file):
    coordFile = openFile('coordenadas_meteoNavarra.json')
    unifiedJSON = []
    for cod in coordFile:
        data = unifyData(file, cod['estacion'])
        unifiedJSON.append(data)

    formattedJSON = []
    for line in unifiedJSON:
        lineCoords = searchEstacionCoords(line['estacion'], coordFile)
        datos = []
        for data in line['datos']:
            dato = {
                'fecha y hora': datetime.strptime(data['fecha y hora'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M"),
                'temperatura (ºC)': data['temperatura (ªC)'],
                'humedad (%)': data['humedad relativa (%)'],
                'precipitacion (mm)': data['precipitacion (l/mm^2)'],
                'nivel (m)': None,
                'caudal (m^3/s)': None,
                'radiacion (W/m^2)': data['radiacion global (W/m^2)'],
            }
            datos.append(dato)
        header = {
            'coordenadas': lineCoords,
            'estacion': line['estacion'],
            'datos': datos
        }
        formattedJSON.append(header)
    saveFile('datos_meteoNavarra.json', formattedJSON)


def main():
    file = openFile(DataJSON)
    formatData(file)


if __name__ == '__main__':
    main()