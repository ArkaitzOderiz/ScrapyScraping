import pandas as pd
import io
import requests
import json
from pathlib import Path

with open('codigos_estaciones_chcantabrico.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    for item in data:
        print(item)
        filepath_pluvio = Path(f'datos/datosPluvio/{item["estacion"]}.csv')
        filepath_pluvio.parent.mkdir(parents=True, exist_ok=True)

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
                print(f'Success creating {item["estacion"]}.csv')
                print("-------------------")
                rawData.to_csv(filepath_pluvio, index=False, header=False)
            else:
                print("Error retrieving data: 404")
                print("-------------------")
        else:
            print(f"Error retrieving data: {response_pluvio.status_code}")
            print("-------------------")

