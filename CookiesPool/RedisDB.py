import random
import redis

class RedisClient():
    def __init__(self, type, website):
        '''Initialize RedisDB'''
        self.db = redis.StrictRedis()
        self.type = type
        self.website = website

    def name(self):
        '''Get the name of Hash'''
        return '{}:{}'.format(self.type, self.website)
    
    def set(self, username, value):
        '''Set key value pair'''
        return self.db.hset(self.name(), username, value)
    
    def get(self, username):
        '''Get key value accoding to key name'''
        return self.db.hget(self.name(), username)
    
    def delete(self, username):
        '''Delete record accoding to key name'''
        return self.db.hdel(self.name(), username)
    
    def count(self):
        '''Get number of records '''
        return self.db.hlen(self.name())
    
    def random(self):
        '''Get value randomly'''
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        '''Get all account information'''
        return self.db.hkeys(self.name())

    def all(self):
        '''Get all key value pairs'''
        return self.db.hgetall(self.name())