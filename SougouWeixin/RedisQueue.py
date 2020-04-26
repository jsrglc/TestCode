from pickle import dumps, loads
from redis import StrictRedis
from WeixinRequest import WeixinRequest

REDIS_KEY = 'requests'

class RedisQueue():
    def __init__(self):
        ''' Initialize RedisDB '''
        self.db = StrictRedis()

    def add(self, request):
        '''Add serialized request to queue

        args:
            request: request object
        return:
            success or not
        '''
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False
    
    def pop(self):
        '''Take the next Request and deserialize it

        return:
            Request or not
        '''
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0

'''
if __name__ == "__main__":
    start_url = 'http://www.baidu.com'
    weinxin_request = WeixinRequest(url=start_url, callback=print)

    queue = RedisQueue()
    queue.add(weinxin_request)

    req = queue.pop()
    print('url: ', req.url)
    print('callback: ', req.callback)
    print('method: ', req.method)
    print('headers: ', req.headers)
    print('need_proxy: ', req.need_proxy)
    print('fail_time: ', req.fail_time)
    print('timeout: ', req.timeout)
'''