from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'china': (Rule(LinkExtractor(allow=r'article/.*.html', restrict_xpaths='//div[@id="rank-defList"]//div[@class="item_con"]'), callback='parse_item', follow=True), Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]//a[contains(., "下一页")]')))
}