import scrapy


class ChcantabricoSpiderSpider(scrapy.Spider):
    name = "chcantabrico_spider"
    allowed_domains = ["www.chcantabrico.es"]
    start_urls = ["https://www.chcantabrico.es/nivel-de-los-rios"]

    def parse(self, response):
        rows = response.xpath('//table[@class="tablefixedheader niveles"]/tbody/tr');

        for row in rows:
            paths = row.xpath('./td/a/@href').getall();
            estaciones = row.xpath('./td/a/text()').getall();
            yield {
                'estacion': estaciones[-3],
                'codigo': paths[-1].split("=")[-1],
            }
