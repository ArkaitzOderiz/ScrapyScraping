import pandas as pd
import io
import requests
import json
from pathlib import Path

with open('codigos_estaciones_chcantabrico.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    for item in data:
        print(item)
        filepath_nivel = Path(f'datos/datosNivel/{item["estacion"]}.csv')
        filepath_nivel.parent.mkdir(parents=True, exist_ok=True)

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
                print(f'Success creating {item["estacion"]}.csv')
                print("-------------------")
                rawData.to_csv(filepath_nivel, index=False, header=False)
            else:
                print("Error retrieving data: 404")
                print("-------------------")
        else:
            print(f"Error retrieving data: {response_nivel.status_code}")
            print("-------------------")

