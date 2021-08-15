# -*- coding: utf-8 -*-
import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        res=json.loads(response.body)
        quotes=res.get('quotes')
        for quote in quotes:
            yield{
                'author':quote.get('author').get('name'),
                'tags':quote.get('tags'),
                'quote_text':quote.get('text')
            }