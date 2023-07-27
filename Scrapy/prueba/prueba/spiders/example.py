import scrapy
from scrapy_selenium import SeleniumRequest

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["administracionelectronica.navarra.es"]
    start_urls = ["https://administracionelectronica.navarra.es/aguaEnNavarra/ctaMapa.aspx?IDOrigenDatos=1&IDMapa=1"]
    custom_settings = {
        'FEEDS': {
            'JSONs/Datos/datos_aguaEnNavarra.json': {
                'format': 'json',
            }
        }
    }

    def parse(self, response):
        for link in response.css('dl#navarramap a::attr(href)'):
            if link.get() != 'ctaMapa.aspx?IdMapa=1&IDOrigenDatos=1':
                yield response.follow(link.get(), callback=self.parse_area)

    def parse_area(self, response):
        for link in response.css('area[shape="rect"]::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_estacion)

    def parse_estacion(self, response):
        for link in response.css('div#divResultadosAforo a::attr(href)'):
            yield SeleniumRequest(
                url=response.urljoin(link.get()),
                wait_time=3,
                callback=self.parse_data,
                script='document.querySelector("#btnDatosNumericos").click()',
            )

    def parse_data(self, response):
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
