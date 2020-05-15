# -*- coding: utf-8 -*-
import scrapy, json
from urllib.parse import urlencode
from images360.items import Images360Item

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
        images = json.loads(response.text).get('list')
        for image in images:
            item = Images360Item()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_thumb')
            yield item