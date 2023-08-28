import json
from datetime import datetime
import pandas as pd

jsonsDir = [
    "../JSONs/RawData/datos_aemet.json",
    "../JSONs/RawData/datos_meteoNavarra.json",
    "../Scrapy/aguaEnNavarra/codigos_datos_aguaEnNavarra.json",
    "../JSONs/RawCode/codigos_chcantabrico.json",
]


def openFile(filename):
    with open(f'../JSONs/RawData/{filename}', "r", encoding="utf-8") as f:
        file = json.loads(f.read())
    return file


def saveFile(filename, data):
    with open(f'../JSONs/ParsedData/{filename}', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def searchEstacionCoords(code, coordFile):
    for data in coordFile:
        if data['estacion'] == code:
            return data['coordenadas']


def unifyData(dataFile, cod):
    datos = []
    for line in dataFile:
        if line['estacion'] == cod:
            for data in line['datos']:
                dato = {
                    'fecha y hora': datetime.strptime(data['fecha y hora'], "%d/%m/%Y %H:%M:%S").strftime(
                        "%Y-%m-%d %H:%M"),
                    'temperatura (ºC)': data['temperatura (ªC)'],
                    'humedad (%)': data['humedad relativa (%)'],
                    'precipitacion (mm)': data['precipitacion (l/mm^2)'],
                    'nivel (m)': None,
                    'caudal (m^3/s)': None,
                    'radiacion (W/m^2)': data['radiacion global (W/m^2)'],
                }
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
    saveFile('datos_aemet.json', formattedJSON)


def formatMeteoNavarra(file):
    codes = [x["estacion"] for x in file]
    uniqueCodes = pd.Series(codes).drop_duplicates().tolist()
    formattedJSON = []
    for code in uniqueCodes:
        header = unifyData(file, code)
        formattedJSON.append(header)
    saveFile('datos_meteoNavarra.json', formattedJSON)


def formatAguaEnNavarra(file):
    dataFile = openFile('datos_aguaEnNavarra.json')
    formattedJSON = []
    for line in file:
        lineData = searchEstacionData(line['estacion'], dataFile)
        datos = []
        index = 0
        indexSecundario = 1
        if len(lineData) == 2:
            if len(lineData[0]) < len(lineData[1]):
                index = 1
                indexSecundario = 0
        for data in lineData[index]['datos']:
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
                dato['nivel (m)'] = data['nivel (m)'].replace(',', '.')
            elif 'caudal (m^3/s)' in data:
                dato['caudal (m^3/s)'] = data['caudal (m^3/s)'].replace(',', '.')

            if len(lineData) == 2:
                dateData = searchDateData(lineData[indexSecundario]['datos'], data['fecha y hora'])
                try:
                    if 'nivel (m)' in dateData:
                        dato['nivel (m)'] = dateData['nivel (m)'].replace(',', '.')
                    if 'caudal (m^3/s)' in dateData:
                        dato['caudal (m^3/s)'] = dateData['caudal (m^3/s)'].replace(',', '.')
                except TypeError:
                    pass

            datos.append(dato)
        header = {
            'estacion': line['estacion'],
            'datos': datos
        }
        formattedJSON.append(header)
    saveFile('datos_aguaEnNavarra.json', formattedJSON)


def formatChcantabrico(file):
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
        for data in lineData[index]['datos']:
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
