import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod


class PwSpiderSpider(scrapy.Spider):
    name = "pw_spider"
    allowed_domains = ["administracionelectronica.navarra.es"]
    start_urls = ["https://administracionelectronica.navarra.es/aguaEnNavarra/ctaMapa.aspx?IDOrigenDatos=1&IDMapa=1"]

    def parse(self, response):
        for link in response.css('dl#navarramap a::attr(href)'):
            if link.get() != 'ctaMapa.aspx?IdMapa=1&IDOrigenDatos=1':
                yield response.follow(link.get(), callback=self.parse_area)

    def parse_area(self, response):
        for link in response.css('area[shape="rect"]::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_estacion)

    def parse_estacion(self, response):
        for link in response.css('div#divResultadosAforo a::attr(href)'):
            yield Request(
                url=response.urljoin(link.get()),
                callback=self.parse_data,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[PageMethod('wait_for_selector', '#btnDatosNumericos'),
                                             PageMethod("click", selector="#btnDatosNumericos")],
                    errback=self.errback,
                ),
            )

    def parse_data(self, response):
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