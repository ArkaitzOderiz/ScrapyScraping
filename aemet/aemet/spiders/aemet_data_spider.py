import json

import scrapy


class AemetDataSpiderSpider(scrapy.Spider):
    name = "aemet_data_spider"
    allowed_domains = ["www.aemet.es"]

    def start_requests(self):
        with open("codigos_estaciones_aemet.json", encoding="utf-8") as f:
            data = json.load(f);
            for estacion in data:
                url = f'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=nav&l={estacion["codigo"]}&w=0&datos=det&x=&f=temperatura';
                yield scrapy.Request(url, self.parse);

    def parse(self, response):
        latitud = response.xpath('//span/abbr[@class="latitude"]/text()').get();
        longitud = response.xpath('//span/abbr[@class="longitude"]/text()').get();
        municipio = response.xpath('//div[@class="contenedor_central_izq marginbottom35px"]/div[@class="notas_tabla"]/a[2]/text()').get();
        fechas = response.xpath('//table/tbody/tr/td[1]/text()').getall();
        precipitacion = response.xpath('//table/tbody/tr/td[7]/text()').getall();

        precipitaciones = [];
        for i, fecha in enumerate(fechas):

            dato = {
                'fecha': fecha.split(' ')[0],
                'hora': fecha.split(' ')[1],
                'precipitacion': precipitacion[0],
            }

            if dato['precipitacion'] == " ":
                dato['precipitacion'] = "0.0";

            precipitaciones.append(dato);

        yield {
            'latitud': latitud,
            'longitud': longitud,
            'municipio':municipio.split(" ")[0],
            'precipitaciones': precipitaciones,
        }
