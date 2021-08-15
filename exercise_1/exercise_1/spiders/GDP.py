# -*- coding: utf-8 -*-
import scrapy


class GdpSpider(scrapy.Spider):
    name = 'GDP'
    allowed_domains = ['worldpopulationreview.com/']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows=response.xpath("//table/tbody/tr")
        for row in rows:
            country_name=row.xpath(".//td/a/text()").get()
            gdp=row.xpath(".//td[2]/text()").get()
            

            yield {
                'country_name':country_name,
                'gdp_dept':gdp
            }

