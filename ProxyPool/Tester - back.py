from RedisDB import RedisClient
from multiprocessing import Pool as ThreadPool
from functools import partial
import aiohttp 
import asyncio

VALID_STATUS_CODE = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 2

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
    
    async def test_single_proxy(self, proxy):
        '''Test single proxy

        args:
            proxy: proxy
        return:
            None
        '''
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as seesion:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('Testing ', proxy)
                async with seesion.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODE:
                        self.redis.max(proxy)
                        print('Proxy ', proxy, ' is valid, set max score.')
                    else:
                        self.redis.decrease(proxy)
                        print('Response code is not valid. Proxy ', proxy, ' is invalid, decrease score.')
            except:
                self.redis.decrease(proxy)
                print('Proxy response failed. Proxy ', proxy, ' is invalid, decrease score.')
    
def test_batch_proxies(proxies):
    '''Test batch proxy

    args:
        proxies: list of proxies
    return:
        None
    '''
    try:
        print('test_batch_proxies ...')

#            loop = asyncio.get_event_loop()
#            tasks = [self.test_single_proxy(proxy) for proxy in proxies]
#            loop.run_until_complete(asyncio.wait(tasks))
#            loop.close()
    except Exception as e:
        print('Tester encountered an error: ', e.args)
        
#    def run(self):
#        print('Tester is running...')
#        pool = ThreadPool()

#        count = self.redis.count()
#        proxy_batchs = []
#        for i in range(0, 10, BATCH_TEST_SIZE):
#            start, end = i, min(i + BATCH_TEST_SIZE, count) - 1
#            proxy_batchs.append(self.redis.batch(start, end))
#            print(start, end)
#            print(self.redis.batch(start, end))
#            print()

#        print(count)
#        print(proxy_batchs)
#        print()        
#        print(proxy_batchs[0])

#        pool.map(lambda list: list + b'ok', proxy_batchs[0])
#        pool.map(self.test_batch_proxies, proxy_batchs)
#        pool.close()
#        pool.join()

#        strs = [it.decode('utf-8') for it in proxy_batchs[0]]
#        print(strs)
#        print([self.redis.db.zscore('proxies', str) for str in strs])

def change(x):
    return x + b'ok'

if __name__ == "__main__":
    tester = Tester()
#    tester.run()
   
    print('Tester is running...')
    pool = ThreadPool()

    count = tester.redis.count()
    proxy_batchs = []
    for i in range(0, 4, BATCH_TEST_SIZE):
        start, end = i, min(i + BATCH_TEST_SIZE, count) - 1
        proxy_batchs.append(tester.redis.batch(start, end))

    print(count)
    print(proxy_batchs)
    print()        
    print(proxy_batchs[0])

#    pool.map(change, proxy_batchs[0])
    pool.map(partial(test_batch_proxies, tester=tester), proxy_batchs)
    pool.close()
    pool.join()

    strs = [it.decode('utf-8') for it in proxy_batchs[0]]
    print(strs)
    print([tester.redis.db.zscore('proxies', str) for str in strs])