import json
from datetime import datetime
from pathlib import Path

DataJSON = "JSONs/RawCode/codigos_chcantabrico.json"


def openFile(filename):
    with open(f'JSONs/RawData/{filename}', "r", encoding="utf-8") as f:
        file = json.loads(f.read())
    return file


def saveFile(filename, data):
    Path("JSONs/ParsedData").mkdir(parents=True, exist_ok=True)
    with open(f'JSONs/ParsedData/{filename}', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def searchEstacionData(code, dataFile1=[], dataFile2=[]):
    datos = []
    for data in dataFile1:
        if data['estacion'] == code:
            datos.append(data)
    for data in dataFile2:
        if data['estacion'] == code:
            datos.append(data)
    return datos


def searchDateData(dataFile, date):
    for data in dataFile:
        if data['fecha y hora'] == date:
            return data


def formatData(file):
    levelDataFile = openFile('datos_nivel_chcantabrico.json')
    pluvioDataFile = openFile('datos_pluvio_chcantabrico.json')
    formattedJSON = []
    for line in file:
        lineData = searchEstacionData(line['codigo'], levelDataFile, pluvioDataFile)
        datos = []
        index = 0
        indexSecundario = 1
        if len(lineData) == 2:
            if len(lineData[0]) < len(lineData[1]):
                index = 1
                indexSecundario = 0
        for i, data in enumerate(lineData[index]['datos']):
            dato = {
                'fecha y hora': datetime.strptime(data['fecha y hora'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M"),
                'temperatura (ºC)': None,
                'humedad (%)': None,
                'precipitacion (mm)': None,
                'nivel (m)': None,
                'caudal (m^3/s)': None,
                'radiacion (W/m^2)': None,
            }

            if 'nivel (m)' in data:
                dato['nivel (m)'] = data['nivel (m)']
            elif 'precipitacion (mm)' in data:
                dato['precipitacion (mm)'] = data['precipitacion (mm)']

            if len(lineData) == 2:
                try:
                    dateData = lineData[indexSecundario]['datos'][i]
                    if data['fecha y hora'] != dateData['fecha y hora']:
                        dateData = searchDateData(lineData[indexSecundario]['datos'], data['fecha y hora'])
                except IndexError:
                    dateData = searchDateData(lineData[indexSecundario]['datos'], data['fecha y hora'])
                try:
                    if 'nivel (m)' in dateData:
                        dato['nivel (m)'] = dateData['nivel (m)']
                    if 'precipitacion (mm)' in dateData:
                        dato['precipitacion (mm)'] = dateData['precipitacion (mm)']
                except TypeError:
                    pass

            datos.append(dato)
        header = {
            'estacion': line['codigo'],
            'datos': datos
        }
        formattedJSON.append(header)
    saveFile('datos_chcantabrico.json', formattedJSON)


def main():
    with open(DataJSON, "r", encoding="utf-8") as f:
        file = json.loads(f.read())

        formatData(file)


if __name__ == "__main__":
    main()
