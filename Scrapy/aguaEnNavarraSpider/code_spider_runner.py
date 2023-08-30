from aguaEnNavarraSpider.spiders.aguaEnNavarra_code_spider import AguaEnNavarraCodeSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(AguaEnNavarraCodeSpider)
    process.start()


if __name__ == '__main__':
    main()
