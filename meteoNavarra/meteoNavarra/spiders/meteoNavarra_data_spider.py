import datetime
import json

import scrapy

class MeteonavarraDataSpiderSpider(scrapy.Spider):
    name = "meteoNavarra_data_spider"
    allowed_domains = ["meteo.navarra.es"]

    def start_requests(self):

        current_date = datetime.date.today()
        delta = datetime.timedelta(days=1)
        tomorrow_date = current_date + delta
        yesterday_date = current_date - delta
        tomorrow_date_format = tomorrow_date.strftime(" %d%%2F %m%%2F%Y").replace(' 0', '')
        yesterday_date_format = yesterday_date.strftime(" %d%%2F %m%%2F%Y").replace(' 0', '')

        with open("codigos_estaciones_meteoNavarra.json", encoding="utf-8") as f:
            data = json.load(f)
            for estacion in data:
                if(estacion["tipo"] == "'AUTO'"):
                    url = f'http://meteo.navarra.es/estaciones/estacion_datos_m.cfm?IDEstacion={estacion["codigo"]}&p_10=1&p_10=2&p_10=3&p_10=11&fecha_desde={yesterday_date_format}&fecha_hasta={tomorrow_date_format}'
                    yield scrapy.Request(url, self.parse)

    def parse(self, response):
        rows = response.xpath('//table[@class="border"]/tr[not(@bgcolor="#FFFFFF")]')
        estacion = response.xpath('//div[@class="tex"]/table/tr/td/h1[1]/text()').get()

        datos = []
        for row in rows:
            dato = {
                'fecha': row.xpath('./td[1]/text()').get().strip().split(' ')[0],
                'hora': row.xpath('./td[1]/text()').get().strip().split(' ')[1],
                'temperatura (ªC)': row.xpath('./td[2]/font/text()').get(),
                'humedad relativa (%)': row.xpath('./td[3]/font/text()').get(),
                'radiacion global (W/m^2)': row.xpath('./td[4]/font/text()').get(),
                'precipitacion (l/mm^2)': row.xpath('./td[5]/font/text()').get(),
            }

            if(dato['precipitacion (l/mm^2)'] != '- -'):
                datos.append(dato)

        yield {
            'estacion': estacion,
            'datos': datos,
        }
