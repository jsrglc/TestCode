MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

import redis
from random import choice

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        '''Initialization

        args:
            host: Redis host adress
            port: Redis port
            password: Redis password
        '''
        self.db = redis.StrictRedis(host=host, port=port, password=password)
    
    def add(self, proxy, score=INITIAL_SCORE):
        '''add proxy, set score to highest

        args:
            proxy: proxy(eg. 111.111.111.111:1111)
            score: rating of proxy
        return:
            result of operation
        '''
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy : score})
    
    def random(self):
        '''Get the valid proxy randomly. First try to get the highest score proxy. If it doesn't exist, get it according to the ranking. Otherwise, it is abnormal.

        return:
            random and valid proxy
        '''
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                print('no proxy in proxypool')
        
    def decrease(self, proxy):
        '''Deduct one point from the rating of proxy, and delete if it is less than the minimum value.

        args:
            proxy: proxy
        return:
            rating of proxy
        '''
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print(' Proxy: ', proxy, ' Score: ', score, ' decrease one point')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print(' Proxy: ', proxy, ' Score: ', score, ' remove')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        '''Judge whether it exists

        args:
            proxy: proxy
        return:
            whether it exists
        '''
        return not self.db.zscore(REDIS_KEY, proxy) == None
    
    def max(self, proxy):
        '''Set rating of proxy to MAX_SCORE
        
        args:
            proxy: proxy
        return:
            result of setting
        '''
        print(' Proxy: ', proxy, ' is available, set to : ', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy : MAX_SCORE})
    
    def count(self):
        '''Get number of proxies

        return:
            number of proxies
        '''
        return self.db.zcard(REDIS_KEY)
    
    def all(self):
        '''Get all proxies

        return:
            all proxies
        '''
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
    
    def batch(self, start, end):
        '''Get batch of proxies

        args:
            start: start index
            end: end index
        return:
            list of proxies
        '''
        return self.db.zrevrange(REDIS_KEY, start, end)