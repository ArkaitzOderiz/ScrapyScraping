import scrapy


class AguaEnNavarraCodeSpider(scrapy.Spider):
    name = "aguaEnNavarra_code_spider"
    allowed_domains = ["administracionelectronica.navarra.es"]
    start_urls = ["https://administracionelectronica.navarra.es/aguaEnNavarra/ctaMapa.aspx?IDOrigenDatos=1&IDMapa=1"]
    custom_settings = {
        'FEEDS': {
            'JSONs/RawCode/codigos_aguaEnNavarra.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
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
        urls = response.xpath('//span/a/@href').getall()
        estacion = response.css('div#bloq_iconos span span::text').getall()
        codigoEstacion = response.css("form#frmDatosEstacion::attr(action)").get()
        codigos = []
        for url in urls:
            codigos.append(url.split('=')[1])

        yield {
            'descripcion': estacion[0],
            'municipio': estacion[1],
            'rio': estacion[2],
            'coordenadas': estacion[3],
            'estacion': codigoEstacion.split('=')[-1],
            'codigos': codigos,
        }
