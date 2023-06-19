import json

import scrapy


class ChcantabricoCoordSpiderSpider(scrapy.Spider):
    name = "chcantabrico_coord_spider"
    allowed_domains = ["ceh.cedex.es"]

    def start_requests(self):
        with open("codigos_estaciones_chcantabrico.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                url = f'https://ceh.cedex.es/anuarioaforos/afo/estaf-datos.asp?indroea={estacion["codigoSecundario"]}'
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
        longitud = response.css('p::text')[6].get().strip()
        latitud = response.css('p::text')[7].get().strip()
        estacion = response.css('font::text')[14].get().strip()

        yield {
            'coordenadas': latitud + ' | ' + longitud,
            'estacion': estacion,
        }
