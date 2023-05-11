import pandas as pd
import io
import requests
import json

with open('codigos_estaciones_chcantabrico.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    datos = []

    for item in data:

        params_pluvio = {
            'p_p_id': 'GraficaEstacion_INSTANCE_ND81Xo17PIZ7',
            'p_p_lifecycle': '2',
            'p_p_state': 'normal',
            'p_p_mode': 'view',
            'p_p_resource_id': 'downloadCsvPluvio',
            'p_p_cacheability': 'cacheLevelPage',
            '_GraficaEstacion_INSTANCE_ND81Xo17PIZ7_cod_estacion': f'{item["codigo"]}',
            '_GraficaEstacion_INSTANCE_ND81Xo17PIZ7_tipodato': 'pluvio',
        }

        response_pluvio = requests.get('https://www.chcantabrico.es/precipitacion-acumulada', params=params_pluvio)
        if response_pluvio.status_code == 200:
            if not response_pluvio.text.startswith('-'):
                urlData = response_pluvio.text
                rawData = pd.read_csv(io.StringIO(urlData), delimiter=';', encoding='utf-8', header=1)
                rawData[['FECHA', 'HORA']] = rawData['FECHA'].str.split(expand=True)
                rawData = rawData.reindex(columns=['FECHA', 'HORA', 'VALOR(mm)'])
                rawData.columns = ['Fecha', 'Hora', 'Valor (mm)']
                parsedData = rawData.to_json(orient="records")

                estacion = {
                    'estacion': item["estacion"],
                    'datos': json.loads(parsedData)
                }
                datos.append(estacion)
            else:
                print(f'{item["estacion"]} Error retrieving data: 404')
                print("-------------------")
        else:
            print(f'{item["estacion"]} Error retrieving data: {response_pluvio.status_code}')
            print("-------------------")

    with open('datos_pluvio_chcantabrico.json', 'w', encoding='utf-8') as outfile:
        json.dump(datos, outfile)

