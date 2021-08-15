# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookShellSpider(CrawlSpider):
    name = 'book_shell'
    allowed_domains = ['books.toscrape.com']

    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'

    def start_request(self):
        yield scrapy.Request(url='https://books.toscrape.com',headers={
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']/article/h3/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), process_request='set_user_agent')
    )
    def set_user_agent(self,request):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        yield{
            'book_name':response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            'book_price':response.xpath("//div[@class='col-sm-6 product_main']/p/text()").get(),
            'book_available':response.xpath("normalize-space(//p[@class='instock availability']/text()[2])").get(),
            'user_agent':response.request.headers['User-Agent']
        }