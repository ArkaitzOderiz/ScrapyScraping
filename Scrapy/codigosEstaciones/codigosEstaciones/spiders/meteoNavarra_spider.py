import scrapy


class MeteonavarraSpider(scrapy.Spider):
    name = "meteoNavarra_spider"
    allowed_domains = ["meteo.navarra.es"]
    start_urls = ["http://meteo.navarra.es/estaciones/mapadeestaciones.cfm#"]
    custom_settings = {
        'FEEDS': {
            '../../JSONs/RawCode/codigos_meteoNavarra.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        rows = response.xpath('//div[@style="margin-left:5px;display:none;"]/script/text()').getall()

        for row in rows:
            if row.split(',')[4].split(')')[0] == "'AUTO'":
                yield {
                    'estacion': row.split(',')[3],
                    'codigo': row.split(',')[0].split('(')[1],
                }
