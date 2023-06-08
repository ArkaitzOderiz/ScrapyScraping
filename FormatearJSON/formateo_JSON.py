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
                'fecha': data['fecha'],
                'hora': data['hora'],
                'temperatura (ºC)': data['temperatura (ºC)'],
                'humedad (%)': data['humedad (%)'],
                'precipitacion (mm)': data['precipitacion (mm)'],
                'nivel (m)': None,
                'caudal (m^3/s)': None,
                'radiacion (W/m^2)': None,
            }
            datos.append(dato)
        header = {
            'coordenadas': line['latitud'] + ' - ' + line['longitud'],
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
                'fecha': data['fecha'],
                'hora': data['hora'],
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


def searchAguaEnNavarraData(dataFile, code):
    datos = []
    for data in dataFile:
        if data['estacion'] == code:
            datos.append(data)
    with open('p.json', 'w', encoding='utf-8') as outfile:
        json.dump(datos, outfile)
    return datos


def formatAguaEnNavarra(file):
    with open('../Scrapy/aguaEnNavarra/datos_aguaEnNavarra.json', "r", encoding="utf-8") as f:
        dataFile = json.loads(f.read())
    formatedJSON = []
    for line in file:
        lineData = searchAguaEnNavarraData(dataFile, line['estacion'])
        datos = []
        if len(lineData) == 1:
            for data in lineData[0]['datos']:
                dato = {
                    'fecha': data['fecha'],
                    'hora': data['hora'],
                    'temperatura (ºC)': None,
                    'humedad (%)': None,
                    'precipitacion (mm)': None,
                    'nivel (m)': None,
                    'caudal (m^3/s)': None,
                    'radiacion (W/m^2)': None,
                }

                if 'nivel (m)' in data:
                    dato['nivel (m)'] = data['nivel (m)']
                if 'caudal (m^3/s)' in data:
                    dato['caudal (m^3/s)'] = data['caudal (m^3/s)']

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
