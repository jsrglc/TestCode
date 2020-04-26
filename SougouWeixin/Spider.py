from requests import Session
from RedisQueue import RedisQueue
from WeixinRequest import WeixinRequest
from GetRandomProxy import Random_Proxy
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from MySQL import MySQL

MAX_FAILED_TIME = 1
VALID_STATUSES = [200]

class Spider():
    base_url = 'https://weixin.sogou.com'
    keyword = 'NBA'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'SUV=1582017065692145; SMYUV=1582017065693186; UM_distinctid=1705790b37e240-00705aeb8c242b-33365801-e1000-1705790b380bb; CXID=9548470635DC4B38B5F6E16346A2E3BE; SUID=0B13DD3A3565860A5E4E53C30003B88F; ad=AD9JSlllll2WPZF6lllllVfYGPclllllnHTnOyllllGlllll9llll5@@@@@@@@@@; ABTEST=6|1587458795|v1; IPLOC=CN3206; weixinIndexVisited=1; SNUID=44266A0DD3D77123E0EC3604D3EE9918; sct=1; JSESSIONID=aaa6T4rpq9IWvaGhDpBgx',
        'Host': 'weixin.sogou.com',
        'Referer': 'https://weixin.sogou.com/weixin?query=NBA&type=2&page=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    session = Session()
    queue = RedisQueue()
    mysql = MySQL()
    random_proxy = Random_Proxy()

    def start(self):
        '''Initialize'''
        self.session.headers.update(self.headers)
        start_url = self.base_url + '/weixin?' + urlencode({
            'query': self.keyword,
            'type': 2,
            'ie': 'utf8'
        })
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        # first request
        self.queue.add(weixin_request)

    def schedule(self):
        '''Scheduling requests'''
        while not self.queue.empty():
            weixin_request = self.queue.pop()

            print('Schedule ', weixin_request.url)
            response = self.request(weixin_request)

            callback = weixin_request.callback

            print(response.status_code)
            print(response.text[:3000])
            print('...0...')

            if response and response.status_code in VALID_STATUSES:
                print('...1...')
                results = list(callback(response))
                if results:
                    print('...2...')
                    for result in results:
                        if isinstance(result, WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            self.mysql.insert('articles', result)
                else:
                    print('...3...')
                    self.error(weixin_request)
            else:
                print('...4...')
                self.error(weixin_request)
    
    def request(self, weixin_request):
        '''Execute request

        args:
            weixin_request: request
        return:
            response
        '''
        try:
#            if weixin_request.need_proxy:
#                proxy = self.random_proxy.get_proxy()

#                print('proxy: ', proxy)

#                if proxy:
#                    proxies = {
#                        'http': 'http://' + proxy,
#                        'https': 'https://' + proxy
#                    }
#                    return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False, proxies=proxies)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False)
        except Exception as e:
            print('request Error: ', e.args)
            return False
    
    def error(self, weixin_request):
        '''Handling of page access error'''
        weixin_request.fail_time = weixin_request.fail_time + 1
        print('Request Failed ', weixin_request.fail_time, ' Times', weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(weixin_request)
    
    def parse_index(self, response):
        '''Parse the index page

        args:
            response: response
        return:
            next response
        '''
        doc = pq(response.text)
        items = doc('#main > div.news-box > ul > li').items
        for item in items:
            url =  self.base_url + item.find('.txt-box > h3 > a').attr('href')
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            yield weixin_request
        
#        next = doc('#sogou_next').attr('href')
#        if next:
#            url = self.base_url + '/weixin' + next
#            weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
#            yield weixin_request

    def parse_detail(self, response):
        '''Parse the information

        args:
            response: response
        return:
            articles
        '''
        doc = pq(response.text)
        articles = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#publish_time').text(),
            'nickname': doc('.rich_media_meta.rich_media_meta_text').text(),
            'wechat': doc('#js_name').text()
        }
        yield articles

    def run(self):
        '''Entry point'''
        self.start()
        self.schedule()

if __name__ == "__main__":
    spider = Spider()
    spider.run()