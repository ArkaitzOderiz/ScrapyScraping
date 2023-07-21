import json

import scrapy
from scrapy import Request


class AguaennavarraDataSpider(scrapy.Spider):
    name = "aguaEnNavarra_data_spider2"
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
                            playwright_include_page=True,
                            errback=self.errback,
                        )
                    )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        estacion = response.css('form#formGrafico::attr(action)').get().split('=')[-1]
        yield Request(
            response.urljoin(f'./ctaDatosGrafico.aspx?IDEstacionSenal={estacion}'),
            callback=self.parse_data,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
            )
        )

    async def parse_data(self, response):
        page = response.meta["playwright_page"]
        await page.close()

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

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
