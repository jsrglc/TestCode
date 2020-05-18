# -*- coding: utf-8 -*-
import scrapy
from scrapyseleniumtest.items import ProductItem
from urllib.parse import quote

class TabaoSpider(scrapy.Spider):
    name = 'tabao'
    allowed_domains = ['www.taobao.com']

    def start_requests(self):
        base_url = 'https://s.taobao.com/search?q='
        
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = base_url + quote(keyword)
                yield scrapy.Request(url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        products = response.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        for product in products:
            item = ProductItem()
            item['image'] = response.urljoin(product.xpath('//div[@class="pic"]//a//img/@data-src').extract_first().strip())
            item['price'] = product.xpath('//div[contains(@class, "price"]/strong/text()').extract_first().strip()
            item['deal'] = product.xpath('//div[@class="deal-cnt"]/text()').extract_first().strip()[:-3]
            item['title'] = ''.join(product.xpath('//*[contails(@class, "title")]/a/span/text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('//div[@class="shop"]/a/span/text()').extract()).strip()
            item['location'] = product.xpath('//div[@class="location"]/text()').extract_first().strip()

            print('item: ', item)

            yield item