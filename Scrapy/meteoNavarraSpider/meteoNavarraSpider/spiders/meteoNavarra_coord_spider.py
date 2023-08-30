import json

import scrapy


class MeteonavarraCoordSpider(scrapy.Spider):
    name = "meteoNavarra_coord_spider"
    allowed_domains = ["meteo.navarra.es"]
    custom_settings = {
        'FEEDS': {
            'JSONs/RawData/coordenadas_meteoNavarra.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        }
    }

    def start_requests(self):
        with open("JSONs/RawCode/codigos_meteoNavarra.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                url = f'http://meteo.navarra.es/estaciones/estacion.cfm?IDestacion={estacion["codigo"]}'
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
        coordenadas = response.css('td::text')[19].get()
        estacion = response.css('input::attr(value)').get()

        yield {
            'coordenadas': coordenadas.strip().replace('\r\n\t\t', ' ').replace(' (*)', ''),
            'estacion': estacion,
        }

