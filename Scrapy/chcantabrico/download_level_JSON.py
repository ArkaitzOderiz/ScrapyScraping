import pandas as pd
import io
import requests
import json

with open('codigos_estaciones_chcantabrico.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    datos = []

    for item in data:

        params_nivel = {
            'p_p_id': 'GraficaEstacion_INSTANCE_wH0LL6jTUysu',
            'p_p_lifecycle': '2',
            'p_p_state': 'normal',
            'p_p_mode': 'view',
            'p_p_resource_id': 'downloadCsv',
            'p_p_cacheability': 'cacheLevelPage',
            '_GraficaEstacion_INSTANCE_wH0LL6jTUysu_cod_estacion': f'{item["codigo"]}',
            '_GraficaEstacion_INSTANCE_wH0LL6jTUysu_tipodato': 'nivel',
        }

        response_nivel = requests.get('https://www.chcantabrico.es/evolucion-de-niveles', params=params_nivel)
        if response_nivel.status_code == 200:
            if not response_nivel.text.startswith('-'):
                urlData = response_nivel.text
                rawData = pd.read_csv(io.StringIO(urlData), delimiter=';', encoding='utf-8', header=1)
                rawData[['FECHA', 'HORA']] = rawData['FECHA'].str.split(expand=True)
                rawData = rawData.reindex(columns=['FECHA', 'HORA', 'VALOR(m)'])
                rawData.columns = ['Fecha', 'Hora', 'Valor (m)']
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
            print(f'{item["estacion"]} Error retrieving data: {response_nivel.status_code}')
            print("-------------------")

    with open('datos_nivel_chcantabrico.json', 'w', encoding='utf-8') as outfile:
        json.dump(datos, outfile)
