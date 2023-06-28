import io
import json

import pandas as pd
import scrapy


class ChcantabricoCoordSpiderSpider(scrapy.Spider):
    name = "chcantabrico_nivel_spider"
    allowed_domains = ["www.chcantabrico.es"]
    custom_settings = {
        'FEEDS': {
            '../../JSONs/RawData/datos_nivel_chcantabrico.json': {
                'format': 'json',
                'overwrite': True,
            }
        }
    }

    def start_requests(self):
        with open("codigos_estaciones_chcantabrico.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                params_nivel = {
                    'p_p_id': 'GraficaEstacion_INSTANCE_wH0LL6jTUysu',
                    'p_p_lifecycle': '2',
                    'p_p_state': 'normal',
                    'p_p_mode': 'view',
                    'p_p_resource_id': 'downloadCsv',
                    'p_p_cacheability': 'cacheLevelPage',
                    '_GraficaEstacion_INSTANCE_wH0LL6jTUysu_cod_estacion': f'{estacion["codigo"]}',
                    '_GraficaEstacion_INSTANCE_wH0LL6jTUysu_tipodato': 'nivel',
                }
                url = 'https://www.chcantabrico.es/evolucion-de-niveles'
                yield scrapy.FormRequest(url=url,
                                         method='GET',
                                         formdata=params_nivel,
                                         callback=self.parse,
                                         cb_kwargs={'estacion': estacion['codigo']}
                )

    def parse(self, response, estacion):
        if not response.text.startswith('-'):
            urlData = response.text
            rawData = pd.read_csv(io.StringIO(urlData), delimiter=';', encoding='utf-8', header=1)
            rawData.columns = ['fecha y hora', 'nivel (m)']
            parsedData = rawData.to_json(orient="records")

            yield {
                'estacion': estacion,
                'datos': json.loads(parsedData)
            }
