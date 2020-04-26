from RedisDB import RedisClient
from multiprocessing import Pool as ThreadPool
from functools import partial
import aiohttp 
import asyncio, selectors

VALID_STATUS_CODE = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 30
   
#async def test_single_proxy(redis, proxy):  
async def test_single_proxy(proxy):
    '''Test single proxy

    args:
        redis: name of redisDB
        proxy: proxy
    return:
        None
    '''
    redis = RedisClient()
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as seesion:
        try:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://' + proxy
            print('Testing ', proxy)
            async with seesion.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                if response.status in VALID_STATUS_CODE:
                    redis.max(proxy)
                    print('Proxy ', proxy, ' is valid, set max score.')
                else:
                    redis.decrease(proxy)
                    print('Response code is not valid. Proxy ', proxy, ' is invalid, decrease score.')
        except:
            redis.decrease(proxy)
            print('Proxy response failed. Proxy ', proxy, ' is invalid, decrease score.')
    
def test_batch_proxies(proxies):
    '''Test batch proxy

    args:
        proxies: list of proxies
    return:
        None
    '''
    try:
#        redis = RedisClient()
#        loop = asyncio.get_event_loop()
        selector = selectors.SelectSelector()
        loop = asyncio.SelectorEventLoop(selector)

#        partial_func = partial(test_single_proxy, redis)
#        tasks = [partial_func(proxy) for proxy in proxies]
        tasks = [test_single_proxy(proxy) for proxy in proxies]

        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
    except Exception as e:
        print('Tester encountered an error: ', e.args)

def tester_run():
    print(' Tester is running...')
    
    redis = RedisClient()
    count = redis.count()
    proxy_batchs = []
    for i in range(0, count, BATCH_TEST_SIZE):
        start, end = i, min(i + BATCH_TEST_SIZE, count) - 1
        proxy_batchs.append(redis.batch(start, end))
    
    pool = ThreadPool()
    pool.map(test_batch_proxies, proxy_batchs)
    pool.close()
    pool.join()

#    strs = [it.decode('utf-8') for it in proxy_batchs[0]]
#    print(strs)
#    print([redis.db.zscore('proxies', str) for str in strs])

if __name__ == "__main__":
    tester_run()