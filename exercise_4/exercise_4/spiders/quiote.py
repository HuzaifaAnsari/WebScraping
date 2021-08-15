# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuioteSpider(scrapy.Spider):
    name = 'quiote'
    allowed_domains = ['quotes.toscrape.com']
    

    script = '''
        function main(splash, args)
            url=args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            assert(splash:set_viewport_full())
            return splash:html()
        
        end
    
    '''
    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com', callback=self.parse, endpoint="execute", args={
            'lua_source':self.script
        })

    def parse(self, response):
        for quotes in response.xpath("//div[@class='quote']"):
            yield {
                'Quotes': quotes.xpath(".//span[@class='text']/text()").get(),
                'authore': quotes.xpath(".//small[@class='author']/text()").get(),
                'tags': quotes.xpath(".//div[@class='tags']/a/text()").getall()
            }
        
        next_page=response.xpath("//li[@class='next']/a/@href").get()
        

        if next_page:
            absolute_url=f"http://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=absolute_url, callback=self.parse, endpoint="execute", args={
                'lua_source':self.script
            })
