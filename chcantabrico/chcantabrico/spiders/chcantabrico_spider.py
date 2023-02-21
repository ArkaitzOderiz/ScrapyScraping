import scrapy


class ChcantabricoSpiderSpider(scrapy.Spider):
    name = "chcantabrico_spider"
    allowed_domains = ["www.chcantabrico.es"]
    start_urls = ["http://www.chcantabrico.es/nivel-de-los-rios"]

    def parse(self, response):
        rows = response.xpath('//table[@class="tablefixedheader niveles"]/tbody/tr');

        for row in rows:
            path = row.xpath('./td/a/@href').getall();
            for url in path:
                yield {
                    'url': url,
                }
