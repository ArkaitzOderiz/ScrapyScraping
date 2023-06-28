import scrapy


class ChcantabricoSpiderSpider(scrapy.Spider):
    name = "chcantabrico_spider"
    allowed_domains = ["www.chcantabrico.es"]
    start_urls = ["https://www.chcantabrico.es/nivel-de-los-rios"]
    custom_settings = {
        'FEEDS': {
            '../../JSONs/Codigos/codigos_chcantabrico.json': {
                'format': 'json',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        rows = response.xpath('//table[@class="tablefixedheader niveles"]/tbody/tr')

        for row in rows:
            codigoBusqueda = row.css('td.codigo::text').get()
            limites = row.css('table.umbrales_gr td.datos::text').getall()
            paths = row.xpath('./td/a/@href').getall()
            estaciones = row.xpath('./td/a/text()').getall()

            for i in range(len(limites)):
                if limites[i] == 'No definido':
                    limites[i] = None

            yield {
                'estacion': estaciones[-3],
                'codigo': paths[-1].split("=")[-1],
                'codigoSecundario': codigoBusqueda,
                'seguimiento': limites[0],
                'prealerta': limites[1],
                'alerta': limites[2],
            }
