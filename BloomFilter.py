import redis

BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 5

class HashMap():
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed
    
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed*ret + ord(value[i])
        return (self.m - 1) & ret

class BloomFilter():
    def __init__(self, server, key, bit=BLOOMFILTER_BIT, hash_number=BLOOMFILTER_HASH_NUMBER):
        self.m = 1 << bit
        self.seeds = range(hash_number)
        self.maps = [HashMap(self.m, seed) for seed in self.seeds]
        self.server = server
        self.key = key
