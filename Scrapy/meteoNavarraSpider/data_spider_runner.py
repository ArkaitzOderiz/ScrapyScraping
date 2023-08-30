from meteoNavarraSpider.spiders.meteoNavarra_data_spider import MeteonavarraDataSpider
from meteoNavarraSpider.spiders.meteoNavarra_coord_spider import MeteonavarraCoordSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(MeteonavarraDataSpider)
    process.crawl(MeteonavarraCoordSpider)
    process.start()


if __name__ == '__main__':
    main()
