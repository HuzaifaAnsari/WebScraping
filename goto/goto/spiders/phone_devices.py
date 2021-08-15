# -*- coding: utf-8 -*-
import scrapy


class PhoneDevicesSpider(scrapy.Spider):
    name = 'phone_devices'
    allowed_domains = ['www.goto.com.pk']

    def start_requests(self):
        yield scrapy.Request(url='https://www.goto.com.pk/phones-devices/', callback=self.parse, headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'})

    def parse(self, response):
        for product in response.xpath('//div[@class="item"]'):
            yield {
                'title': product.xpath('.//div[@class="product-image preloader"]/a/@title').get(),
                'url': product.xpath('.//div[@class="product-image preloader"]/a/@href').get(),
                'product_price': product.xpath('.//span[@class="regular-price"]/span/text()[normalize-space()]')[0].get().strip(),
                'rating_reviews': product.xpath('.//span[@class="count float-right"]/a/text()').get(),
                'User-Agent':response.request.headers['User-Agent']
            }

        next_page=response.urljoin(response.xpath('//li[@class="next"]/a/@href').get())
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'}
                )