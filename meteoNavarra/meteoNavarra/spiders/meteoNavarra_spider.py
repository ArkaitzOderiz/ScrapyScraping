import scrapy


class MeteonavarraSpiderSpider(scrapy.Spider):
    name = "meteoNavarra_spider"
    allowed_domains = ["meteo.navarra.es"]
    start_urls = ["http://meteo.navarra.es/estaciones/mapadeestaciones.cfm#"]

    def parse(self, response):
        rows = response.xpath('//div[@style="margin-left:5px;display:none;"]/script/text()').getall();

        for row in rows:
            yield {
                'estacion': row.split(',')[3],
                'codigo': row.split(',')[0].split('(')[1],
                'tipo': row.split(',')[4].split(')')[0],
            }
