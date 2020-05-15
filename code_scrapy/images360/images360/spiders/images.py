# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def start_requests(self):
        data = {
            'ch': 'photography',
            'listtype': 'new',
            'temp': 1
        }
        base_url = 'https://image.so.com/zjl?'
        for page in range(1, self.settings.get('MAX_PAGE')+1):
            data['sn'] = page * 30
            url = base_url + urlencode(data)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        pass
