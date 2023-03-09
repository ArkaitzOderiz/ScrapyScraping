import json

import scrapy


class AguaennavarraDataSpiderSpider(scrapy.Spider):
    name = "aguaEnNavarra_data_spider"
    allowed_domains = ["administracionelectronica.navarra.es"]


    def start_requests(self):
        with open("codigos_datos_aguaEnNavarra.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                for codigo in estacion['codigos']:
                    url = f'https://administracionelectronica.navarra.es/aguaEnNavarra/ctaDatosEstacion.aspx?IdEstacion={codigo}'
                    yield scrapy.Request(url, self.parse)

    def parse(self, response):
        tipo = response.xpath('//span[@id="lblSenal"]/text()').get()
        estacion = response.xpath('//div[@id="bloq_iconos"]/div/span/span/text()').get()
