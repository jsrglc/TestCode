# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    base_urls = 'http://www.baidu.com/s?wd='

    def start_requests(self):
        for i in range(10):
            url = self.base_urls + str(i)
            yield scrapy.Request(url, callback=self.parse)

        for i in range(30):
            url = self.base_urls + str(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        pass
