import json

import scrapy


class AemetDataSpider(scrapy.Spider):
    name = "aemet_data_spider"
    allowed_domains = ["www.aemet.es"]
    custom_settings = {
        'FEEDS': {
            'JSONs/RawData/datos_aemet.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        }
    }

    def start_requests(self):
        with open("JSONs/RawCode/codigos_aemet.json", encoding="utf-8") as f:
            data = json.load(f)
        for estacion in data:
            url = f'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=nav&l={estacion["codigo"]}&w=0&datos=det&x=&f=temperatura'
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        latitud = response.css('abbr.latitude::text').get()
        longitud = response.css('abbr.longitude::text').get()
        estacion = response.css("a.separador_pestanhas").get()
        rows = response.css('tbody tr')

        datos = []
        for row in rows:
            dato = {
                'fecha y hora': row.xpath('./td[1]/text()').get() + ':00',
                'temperatura (ºC)': row.xpath('./td[2]/text()').get(),
                'humedad (%)': row.xpath('./td[10]/text()').get(),
                'precipitacion (mm)': row.xpath('./td[7]/text()').get(),
            }

            if dato['precipitacion (mm)'] != " ":
                datos.append(dato)

        yield {
            'coordenadas': latitud + ' | ' + longitud,
            'estacion': estacion.split('=')[3].split('&')[0],
            'datos': datos,
        }
