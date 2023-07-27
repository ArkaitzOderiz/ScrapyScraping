from datosEstaciones.spiders.aemet_spider import AemetDataSpider
from datosEstaciones.spiders.chcantabrico_pluvio_spider import ChcantabricoPluvioSpider
from datosEstaciones.spiders.chcantabrico_nivel_spider import ChcantabricoNivelSpider
from datosEstaciones.spiders.chcantabrico_coord_spider import ChcantabricoCoordSpider
from datosEstaciones.spiders.meteoNavarra_coord_spider import MeteonavarraCoordSpider
from datosEstaciones.spiders.meteoNavarra_spider import MeteonavarraDataSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(AemetDataSpider)
    process.crawl(ChcantabricoPluvioSpider)
    process.crawl(ChcantabricoNivelSpider)
    process.crawl(MeteonavarraDataSpider)
    process.crawl(MeteonavarraCoordSpider)
    process.crawl(ChcantabricoCoordSpider)
    process.start()


if __name__ == '__main__':
    main()
