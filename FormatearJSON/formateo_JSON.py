import json

jsonsDir = [
    "../Scrapy/aemet/datos_aemet.json",
    "../Scrapy/meteoNavarra/datos_meteoNavarra.json",
    "../Scrapy/aguaEnNavarra/codigos_datos_aguaEnNavarra.json",
    "../Scrapy/chcantabrico/codigos_estaciones_chcantabrico.json",
]


def formatAemet(file):
    formatedJSON = []
    for line in file:
        datos = []
        for data in line['datos']:
            dato = {
                'fecha y hora': data['fecha y hora'],
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
        formatedJSON.append(header)
    with open('datos_aemet.json', 'w', encoding='utf-8') as outfile:
        json.dump(formatedJSON, outfile)


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


def formatMeteoNavarra(file):
    with open('../Scrapy/meteoNavarra/coordenadas_meteoNavarra.json', "r", encoding="utf-8") as f:
        coordFile = json.loads(f.read())

    unifiedJSON = []
    for cod in coordFile:
        data = unifyData(file, cod['estacion'])
        unifiedJSON.append(data)

    formatedJSON = []
    for line in unifiedJSON:
        lineCoords = searchEstacionCoords(line['estacion'], coordFile)
        datos = []
        for data in line['datos']:
            dato = {
                'fecha y hora': data['fecha y hora'],
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
        formatedJSON.append(header)
    with open('datos_meteoNavarra.json', 'w', encoding='utf-8') as outfile:
        json.dump(formatedJSON, outfile)


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


def formatAguaEnNavarra(file):
    with open('../Scrapy/aguaEnNavarra/datos_aguaEnNavarra.json', "r", encoding="utf-8") as f:
        dataFile = json.loads(f.read())
    formatedJSON = []
    for line in file:
        lineData = searchEstacionData(line['estacion'], dataFile)
        datos = []
        index = 0
        indexSecundario = 1
        if len(lineData) == 2:
            if len(lineData[0]) < len(lineData[1]):
                index = 1
                indexSecundario = 0
        for i, data in enumerate(lineData[index]['datos']):
            dato = {
                'fecha y hora': data['fecha y hora'],
                'temperatura (ºC)': None,
                'humedad (%)': None,
                'precipitacion (mm)': None,
                'nivel (m)': None,
                'caudal (m^3/s)': None,
                'radiacion (W/m^2)': None,
            }

            if 'nivel (m)' in data:
                dato['nivel (m)'] = data['nivel (m)']
            elif 'caudal (m^3/s)' in data:
                dato['caudal (m^3/s)'] = data['caudal (m^3/s)']

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
                    if 'caudal (m^3/s)' in dateData:
                        dato['caudal (m^3/s)'] = dateData['caudal (m^3/s)']
                except TypeError:
                    pass

            datos.append(dato)
        header = {
            'coordenadas': line['coordenadas'],
            'estacion': line['estacion'],
            'datos': datos
        }
        formatedJSON.append(header)
    with open('datos_aguaEnNavarra.json', 'w', encoding='utf-8') as outfile:
        json.dump(formatedJSON, outfile)


def formatChcantabrico(file):
    with open('../Scrapy/chcantabrico/datos_nivel_chcantabrico.json', "r", encoding="utf-8") as f:
        levelDataFile = json.loads(f.read())
    with open('../Scrapy/chcantabrico/datos_pluvio_chcantabrico.json', "r", encoding="utf-8") as f:
        pluvioDataFile = json.loads(f.read())
    formatedJSON = []
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
                'fecha y hora': data['fecha y hora'],
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
                        dato['complement'] = dateData['fecha y hora']
                    if 'precipitacion (mm)' in dateData:
                        dato['precipitacion (mm)'] = dateData['precipitacion (mm)']
                        dato['complement'] = dateData['fecha y hora']
                except TypeError:
                    pass

            datos.append(dato)
        header = {
            'coordenadas': None,
            'estacion': line['codigo'],
            'datos': datos
        }
        formatedJSON.append(header)
    with open('datos_chcantabrico.json', 'w', encoding='utf-8') as outfile:
        json.dump(formatedJSON, outfile)


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
