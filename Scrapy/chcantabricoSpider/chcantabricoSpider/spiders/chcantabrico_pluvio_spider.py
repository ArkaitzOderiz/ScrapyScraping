import io
import json

import pandas as pd
import scrapy


class ChcantabricoPluvioSpider(scrapy.Spider):
    name = "chcantabrico_pluvio_spider"
    allowed_domains = ["www.chcantabrico.es"]
    custom_settings = {
        'FEEDS': {
            'JSONs/RawData/datos_pluvio_chcantabrico.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        }
    }

    def start_requests(self):
        with open("JSONs/RawCode/codigos_chcantabrico.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                params_pluvio = {
                    'p_p_id': 'GraficaEstacion_INSTANCE_ND81Xo17PIZ7',
                    'p_p_lifecycle': '2',
                    'p_p_state': 'normal',
                    'p_p_mode': 'view',
                    'p_p_resource_id': 'downloadCsvPluvio',
                    'p_p_cacheability': 'cacheLevelPage',
                    '_GraficaEstacion_INSTANCE_ND81Xo17PIZ7_cod_estacion': f'{estacion["codigo"]}',
                    '_GraficaEstacion_INSTANCE_ND81Xo17PIZ7_tipodato': 'pluvio',
                }
                url = 'https://www.chcantabrico.es/precipitacion-acumulada'
                yield scrapy.FormRequest(url=url,
                                         method='GET',
                                         formdata=params_pluvio,
                                         callback=self.parse,
                                         cb_kwargs={'estacion': estacion['codigo']}
                )

    def parse(self, response, estacion):
        if not response.text.startswith('-'):
            urlData = response.text
            rawData = pd.read_csv(io.StringIO(urlData), delimiter=';', encoding='utf-8', header=1)
            rawData.columns = ['fecha y hora', 'precipitacion (mm)']
            parsedData = rawData.to_json(orient="records")

            yield {
                'estacion': estacion,
                'datos': json.loads(parsedData)
            }
