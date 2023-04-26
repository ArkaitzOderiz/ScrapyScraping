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

        tipo = response.xpath('//span[@id="lblSenal"]/text()').get()
        estacion = response.xpath('//div[@id="bloq_iconos"]/div/span/span/text()').get()
        fechas = response.xpath('//div[@id="lista"]/span[@class="cont_fecha_gra"]/text()').getall()
        valores = response.xpath('//div[@id="lista"]/span[@class="cont_valor_gra"]/text()').getall()

        datos = []
        for i, fecha in enumerate(fechas):
            dato = {
                'fecha': fecha.strip().split(' ')[0],
                'hora': fecha.strip().split(' ')[1],
                'valor': valores[i].strip(),
            }
            datos.append(dato)

        if tipo == "Nivel Río":
            yield {
                'tipo': tipo,
                'estacion': estacion,
                'nivel (m)': datos,
            }
        else:
            yield {
                'tipo': tipo,
                'estacion': estacion,
                'caudal (m^3/s)': datos,
            }
