# -*- coding: utf-8 -*-
import scrapy


class GlassessshopBestsellersSpider(scrapy.Spider):
    name = 'glassessshop_bestsellers'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']
    #def start_request(self):
     #   yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
      #      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'
       # })

    def parse(self, response):
        for product in response.xpath("//div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']"):
            yield{
                'product_url':product.xpath(".//div[@class='product-img-outer']/a[1]/@href").get(),
                'product_image_link':product.xpath(".//div[@class='product-img-outer']/a[1]/img[1]/@data-src").get(),
                'product_name':product.xpath(".//div[@class='p-title']/a[1]/text()[normalize-space()]")[0].get().strip(),
                'product_price':product.xpath(".//div[@class='p-price']/div[1]/span/text()").get()
            }

        next_page=response.xpath("//div[@class='col-7']/ul/li[position()=(last())]/a/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
