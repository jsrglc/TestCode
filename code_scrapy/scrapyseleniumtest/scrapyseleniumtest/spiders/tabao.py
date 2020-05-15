# -*- coding: utf-8 -*-
import scrapy


class TabaoSpider(scrapy.Spider):
    name = 'tabao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']

    def parse(self, response):
        pass
