# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls=['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']
    
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'

    def start_request(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc', headers={
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"),process_request='set_user_agent')
    )
    def set_user_agent(self,request):
        request.headers['User-Agent']=self.user_agent
        return request


    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='TitleBlock__Container-sc-1nlhx7j-0 hglRHk']/div/h1/text()").get(),
            'year':response.xpath("//div[@class='TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr']/ul/li[1]/span/text()").get(),
            'duration':response.xpath("//div[@class='TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr']/ul/li[3]/text()").get(),
            'genre':response.xpath("//div[@class='ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL']/a/span/text()").get(),
            'rating':response.xpath("//div[@class='AggregateRatingButton__Rating-sc-1ll29m0-2 bmbYRW']/span/text()").get(),
            'movie_url':response.url,
        }
