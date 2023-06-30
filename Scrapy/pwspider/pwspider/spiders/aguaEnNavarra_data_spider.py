import json

import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod


class AguaennavarraDataSpiderSpider(scrapy.Spider):
    name = "aguaEnNavarra_data_spider"
    allowed_domains = ["administracionelectronica.navarra.es"]
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }

    def start_requests(self):
        with open("codigos_datos_aguaEnNavarra.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                for codigo in estacion['codigos']:
                    url = f'https://administracionelectronica.navarra.es/aguaEnNavarra/mostrarGrafico.aspx?IdEstacionSenal={codigo}'

                    yield Request(
                        url=url,
                        callback=self.parse,
                        meta=dict(
                            playwright=True,
                            playwright_page_methods=[
                                PageMethod("wait_for_selector", selector="div.botoneraGrafico", state="visible"),
                                PageMethod("click", selector="input#btnDatosNumericos"),
                                PageMethod("waitForEvent", event="click"),
                                PageMethod("screenshot", path="example.png", full_page=True), ],
                        ),
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
                    'fecha y hora': fecha.strip() + ':00',
                    'nivel (m)': valores[i].strip(),
                }
                datos.append(dato)
        else:
            for i, fecha in enumerate(fechas):
                dato = {
                    'fecha y hora': fecha.strip() + ':00',
                    'caudal (m^3/s)': valores[i].strip(),
                }
                datos.append(dato)

        yield {
            'estacion': estacion.split('=')[-1],
            'datos': datos,
        }
