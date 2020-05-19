# -*- coding: utf-8 -*-
import scrapy
from scrapyseleniumtest.items import ProductItem
from urllib.parse import quote

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['www.dangdang.com']
    base_url = 'http://search.dangdang.com/?key='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.base_url + quote(keyword)
                yield scrapy.Request(url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        products = response.xpath('//*[@id="component_59"]/li')
        for product in products:
            item = ProductItem()
            item['image'] = response.urljoin(product.xpath('.//a[@class="pic"]/img/@src').extract_first().strip())
            item['price'] = product.xpath('.//p[@class="price"]/span/text()').extract_first().strip()[1:]
            item['title'] = ''.join(product.xpath('.//p[@class="name"]/a/text()').extract()).strip()
            item['deal'] = product.xpath('.//p[@class="star"]/a/text()').extract_first().strip()[:-3]
            item['shop'] = product.xpath('.//p[@class="link"]/a/text()').extract_first()
            item['location'] = 'no localtion'

            yield item
