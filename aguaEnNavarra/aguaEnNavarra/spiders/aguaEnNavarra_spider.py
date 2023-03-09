import scrapy


class AguaennavarraSpiderSpider(scrapy.Spider):
    name = "aguaEnNavarra_spider"
    allowed_domains = ["administracionelectronica.navarra.es"]

    def start_requests(self):
        mapas = [2, 3, 4, 5, 6, 7]
        for mapa in mapas:
            url = f'https://administracionelectronica.navarra.es/aguaEnNavarra/ctaMapa.aspx?IdMapa={mapa}&IDOrigenDatos=1'
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        aforo = response.xpath('//div[@id="cabecera_divMigas"]/map/ul/li/ul/li/text()').get().strip()
        urls = response.xpath('//div[@id="divMapa"]/map/area[@shape="rect"]/@href').getall()

        codigos = []
        for url in urls:
            codigos.append(url.split('=')[1])

        yield {
            'aforo': aforo,
            'codigos': codigos,
        }