from RedisDB import RedisClient
from Crawler import Crawler

POOL_UPPER_THRESHOLD = 10000  # maximum number of proxies in the pool

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        '''
        Jude whether the number limit of proxies is reached
        '''
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        crawlerCount = self.crawler.__CrawlFuncCount__
        print('crawlerCount: ', crawlerCount)
        for callback_lable in range(crawlerCount):
            if self.is_over_threshold():
                print('The proxies in the pool is too many!')
                break
            callback = self.crawler.__CrawlFunc__[callback_lable]
            proxies = self.crawler.get_proxies(callback)
            for proxy in proxies:
                self.redis.add(proxy)