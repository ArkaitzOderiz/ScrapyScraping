import scrapy


class AemetCodeSpider(scrapy.Spider):
    name = "aemet_code_spider"
    allowed_domains = ["www.aemet.es"]
    start_urls = ["https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=nav&w=0&datos=det&x=h24&f=temperatura"]
    custom_settings = {
        'FEEDS': {
            'JSONs/RawCode/codigos_aemet.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        rows = response.css("div#contenedor_tabla tbody tr a")

        for row in rows:
            path = row.xpath("@href").get()
            name = row.xpath("./text()").get()
            yield {
                'estacion': name,
                'codigo': path.split('&')[1].split('=')[1],
            }

