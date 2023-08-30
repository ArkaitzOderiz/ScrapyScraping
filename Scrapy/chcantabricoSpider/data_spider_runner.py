from chcantabricoSpider.spiders.chcantabrico_coord_spider import ChcantabricoCoordSpider
from chcantabricoSpider.spiders.chcantabrico_nivel_spider import ChcantabricoNivelSpider
from chcantabricoSpider.spiders.chcantabrico_pluvio_spider import ChcantabricoPluvioSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(ChcantabricoPluvioSpider)
    process.crawl(ChcantabricoNivelSpider)
    process.crawl(ChcantabricoCoordSpider)
    process.start()


if __name__ == '__main__':
    main()
