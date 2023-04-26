import json

import scrapy


class AguaennavarraNewcodSpiderSpider(scrapy.Spider):
    name = "aguaEnNavarra_newCod_spider"
    allowed_domains = ["administracionelectronica.navarra.es"]

    def start_requests(self):
        with open("codigos_estaciones_aguaEnNavarra.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                for codigo in estacion['codigos']:
                    url = f'https://administracionelectronica.navarra.es/aguaEnNavarra/ctaDatosEstacion.aspx?IdEstacion={codigo}'
                    yield scrapy.Request(url, self.parse)

    def parse(self, response):
        urls = response.xpath('//span/a/@href').getall()
        estacion = response.xpath('//div[@id="bloq_iconos"]/div/span/span/text()').getall()

        codigos = []
        for url in urls:
            codigos.append(url.split('=')[1])

        yield {
            'descripcion': estacion[0],
            'municipio': estacion[1],
            'rio': estacion[2],
            'coordenadas': estacion[3],
            'codigos': codigos,
        }
