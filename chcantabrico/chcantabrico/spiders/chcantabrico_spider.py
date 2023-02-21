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
            if(len(paths) == 4):
                yield {
                    'estacion': estaciones[2],
                    'url': paths[2],
                }
            elif(len(paths) == 3):
                yield {
                    'estacion': estaciones[1],
                    'url': paths[1],
                }
            elif(len(paths) == 2):
                yield {
                    'estacion': estaciones[0],
                    'url': paths[0],
                }
