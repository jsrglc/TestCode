# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.items import NewsItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article/.*.html', restrict_xpaths='//div[@id="rank-defList"]//div[@class="item_con"]'), callback='parse_item', follow=True), 
#        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]//a[contains(., "下一页")]'))
    )

    def parse_item(self, response):
#        item = NewsItem()
#        item['title'] = response.xpath('//*[@id="chan_newsTitle"]/text()').get()
#        item['url'] = response.url
#        item['source'] = response.xpath('//*[@id="js-article-title"]//span[@class="source"]/text()').get()[3:].strip()
#        item['datatime'] = response.xpath('//*[@id="js-article-title"]//span[@class="time"]/text()').get()
#        item['text'] = response.xpath('//*[@id="chan_newsDetail"]//p[position() < last()]/text()').getall()
#        item['website'] = 'tech.china.com'
#        return item
        loader = ChinaLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//*[@id="chan_newsTitle"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('text', '//*[@id="chan_newsDetail"]//p[position() < last()]/text()')
        loader.add_xpath('datatime', '//*[@id="js-article-title"]//span[@class="time"]/text()')
        loader.add_xpath('source', '//*[@id="js-article-title"]//span[@class="source"]/text()', re='来源：(.*)')
        loader.add_value('website', 'tech.china.com')

#        print()
#        print(loader.load_item())
#        print(type(loader.load_item()))
#        print(loader.load_item()['title'])
#        print(type(loader.load_item()['title']))
#        print(loader.load_item()['url'])
#        print(type(loader.load_item()['url']))
#        print(loader.load_item()['text'])
#        print(type(loader.load_item()['text']))
#        print(loader.load_item()['datatime'])
#        print(type(loader.load_item()['datatime']))
#        print(loader.load_item()['source'])
#        print(type(loader.load_item()['source']))
#        print()

        yield loader.load_item()
