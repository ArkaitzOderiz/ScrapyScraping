import json
from datetime import datetime

jsonsDir = [
    "../JSONs/RawCode/codigos_aemet.json",
    "../JSONs/RawCode/codigos_meteoNavarra.json",
    "../Scrapy/aguaEnNavarra/codigos_datos_aguaEnNavarra.json",
    "../JSONs/RawCode/codigos_chcantabrico.json",
]


def openFile(filename):
    with open(f'../JSONs/RawData/{filename}', "r", encoding="utf-8") as f:
        file = json.loads(f.read())
    return file


def saveFile(filename, data):
    with open(f'../JSONs/ParsedCode/{filename}', 'w', encoding='utf-8') as outfile:
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


def formatAemet(file):
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


def formatMeteoNavarra(file):
    coordFile = openFile('coordenadas_meteoNavarra.json')
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
    saveFile('codigos_meteoNavarra.json', formattedJSON)


def formatAguaEnNavarra(file):
    formattedJSON = []
    for line in file:
        header = {
            'estacion': line['descripcion'],
            'codigo': line['codigo'],
            'coordenadas': line['coordenadas'],
            'seguimiento': None,
            'prealerta': None,
            'alerta': None,

        }
        formattedJSON.append(header)
    saveFile('codigos_aguaEnNavarra.json', formattedJSON)


def formatChcantabrico(file):
    coordFile = openFile('coordenadas_chcantabrico.json')
    formattedJSON = []
    for line in file:
        lineCoords = searchEstacionCoords(line['codigoSecundario'], coordFile)
        header = {
            'estacion': line['estacion'],
            'codigo': line['codigo'],
            'coordenadas': lineCoords,
            'seguimiento': line['seguimiento'],
            'prealerta': line['prealerta'],
            'alerta': line['alerta'],

        }
        formattedJSON.append(header)
    saveFile('codigos_chcantabrico.json', formattedJSON)


for i, dataJSON in enumerate(jsonsDir):
    with open(dataJSON, "r", encoding="utf-8") as f:
        file = json.loads(f.read())

    if i == 0:
        formatAemet(file)
    elif i == 1:
        formatMeteoNavarra(file)
    elif i == 2:
        formatAguaEnNavarra(file)
    elif i == 3:
        formatChcantabrico(file)
