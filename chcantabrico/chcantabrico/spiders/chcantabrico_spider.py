import scrapy


class ChcantabricoSpiderSpider(scrapy.Spider):
    name = "chcantabrico_spider"
    allowed_domains = ["www.chcantabrico.es"]
    start_urls = ["https://www.chcantabrico.es/nivel-de-los-rios"]

    def parse(self, response):
        rows = response.xpath('//table[@class="tablefixedheader niveles"]/tbody/tr')

        for row in rows:
            limites = row.xpath('./td/table[@class="umbrales_gr"]/tr[3]/td/text()').getall()
            paths = row.xpath('./td/a/@href').getall()
            estaciones = row.xpath('./td/a/text()').getall()
            yield {
                'estacion': estaciones[-3],
                'codigo': paths[-1].split("=")[-1],
                'seguimiento': limites[0],
                'prealerta': limites[1],
                'alerta': limites[2],
            }
