#import redis

BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 10

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

    def exists(self, value):
        if not value:
            return False
        exist = 1
        for map in self.maps:
            offset = map.hash(value)
            exist = exist & self.server.getbit(self.key, offset)
        return exist
    
    def insert(self, value):
        for f in self.maps:
            offset = f.hash(value)
            self.server.setbit(self.key, offset, 1)

'''
if __name__ == "__main__":
    conn = redis.StrictRedis()
    bf = BloomFilter(conn, 'testbf')
    bf.insert('Hello')
    bf.insert('World')
    bf.insert('Python')
    bf.insert('c++')
    result = bf.exists('Hello')
    print(bool(result))
    result = bf.exists('python')
    print(bool(result))
    result = bf.exists('Python')
    print(bool(result))
    result = bf.exists('C++')
    print(bool(result))
    result = bf.exists('pYTHON')
    print(bool(result))
'''