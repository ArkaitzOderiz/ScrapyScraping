import scrapy


class AemetSpider(scrapy.Spider):
    name = "aemet_spider"
    allowed_domains = ["www.aemet.es"]
    start_urls = ["https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=nav&w=0&datos=det&x=h24&f=temperatura"]
    custom_settings = {
        'FEEDS': {
            '../../JSONs/Codigos/codigos_aemet.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        rows = response.xpath('//div[@id="contenedor_tabla"]/table/tbody/tr')

        for row in rows:
            path = row.xpath('./td/a/@href').extract_first()
            name = row.xpath('./td/a/text()').extract_first()
            yield {
                'estacion': name,
                'codigo': path.split('&')[1].split('=')[1],
            }

