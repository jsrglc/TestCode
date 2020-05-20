# -*- coding: utf-8 -*-
import scrapy


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['www.dangdang.com']
    start_urls = ['http://www.dangdang.com/']

    def parse(self, response):
        pass
