import scrapy


class MeteonavarraCodeSpider(scrapy.Spider):
    name = "meteoNavarra_code_spider"
    allowed_domains = ["meteo.navarra.es"]
    start_urls = ["http://meteo.navarra.es/estaciones/mapadeestaciones.cfm#"]
    custom_settings = {
        'FEEDS': {
            'JSONs/RawCode/codigos_meteoNavarra.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        rows = response.css('div#tabAUTO script::text').getall()

        for row in rows:
            yield {
                'estacion': row.split(',')[3],
                'codigo': row.split(',')[0].split('(')[1],
            }
