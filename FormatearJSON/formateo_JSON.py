import json

jsonsDir = [
    "../Scrapy/aemet/datos_aemet.json",
    "../Scrapy/meteoNavarra/datos_meteoNavarra.json",
    "../Scrapy/aguaEnNavarra/codigos_datos_aguaEnNavarra.json"
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
            'coordenadas': line['latitud'] + ' | ' + line['longitud'],
            'estacion': line['estacion'],
            'datos': datos
        }
        formatedJSON.append(header)
    with open('datos_aemet.json', 'w', encoding='utf-8') as outfile:
        json.dump(formatedJSON, outfile)


def formatMeteoNavarra(file):
    formatedJSON = []
    for line in file:
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
            'coordenadas': None,
            'estacion': line['estacion'],
            'datos': datos
        }
        formatedJSON.append(header)
    with open('datos_meteoNavarra.json', 'w', encoding='utf-8') as outfile:
        json.dump(formatedJSON, outfile)


def searchEstacionData(dataFile, code):
    datos = []
    for data in dataFile:
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
        lineData = searchEstacionData(dataFile, line['estacion'])
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


for i, dataJSON in enumerate(jsonsDir):
    with open(dataJSON, "r", encoding="utf-8") as f:
        file = json.loads(f.read())
        if i == 0:
            formatAemet(file)
        elif i == 1:
            formatMeteoNavarra(file)
        elif i == 2:
            formatAguaEnNavarra(file)
