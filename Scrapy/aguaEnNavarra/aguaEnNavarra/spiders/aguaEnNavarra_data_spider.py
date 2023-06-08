import json

import scrapy
from scrapy_selenium import SeleniumRequest


class AguaennavarraDataSpiderSpider(scrapy.Spider):
    name = "aguaEnNavarra_data_spider"
    allowed_domains = ["administracionelectronica.navarra.es"]

    def start_requests(self):
        with open("codigos_datos_aguaEnNavarra.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                for codigo in estacion['codigos']:
                    url = f'https://administracionelectronica.navarra.es/aguaEnNavarra/mostrarGrafico.aspx?IdEstacionSenal={codigo}'

                    yield SeleniumRequest(
                        url=url,
                        wait_time=3,
                        callback=self.parse,
                        script='document.querySelector("#btnDatosNumericos").click()',
                    )

    def parse(self, response):
        tipo = response.css('span#lblSenal::text').get()
        estacion = response.css('li#cabecera_nombreEstacion a::attr(href)').get()
        fechas = response.css('span.cont_fecha_gra::text').getall()
        valores = response.css('span.cont_valor_gra::text').getall()

        datos = []
        if tipo == "Nivel Río":
            for i, fecha in enumerate(fechas):
                dato = {
                    'fecha': fecha.strip().split(' ')[0],
                    'hora': fecha.strip().split(' ')[1],
                    'nivel (m)': valores[i].strip(),
                }
                datos.append(dato)
        else:
            for i, fecha in enumerate(fechas):
                dato = {
                    'fecha': fecha.strip().split(' ')[0],
                    'hora': fecha.strip().split(' ')[1],
                    'caudal (m^3/s)': valores[i].strip(),
                }
                datos.append(dato)

        yield {
            'estacion': estacion.split('=')[-1],
            'datos': datos,
        }
