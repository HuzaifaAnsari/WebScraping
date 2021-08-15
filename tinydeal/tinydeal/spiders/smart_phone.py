# -*- coding: utf-8 -*-
import scrapy


class SmartPhoneSpider(scrapy.Spider):
    name = 'smart_phone'
    allowed_domains = ['www.tinydeals.co/product-category/smart-phones-tablets']
    start_urls = ['http://www.tinydeals.co/product-category/smart-phones-tablets/']

    def parse(self, response):
        pass
