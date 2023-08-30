from chcantabricoSpider.spiders.chcantabrico_coord_spider import ChcantabricoCoordSpider
from chcantabricoSpider.spiders.chcantabrico_code_spider import ChcantabricoCodeSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(ChcantabricoCodeSpider)
    process.start()


if __name__ == '__main__':
    main()
