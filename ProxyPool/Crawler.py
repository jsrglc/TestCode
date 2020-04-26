from pyquery import PyQuery as pq
import time, requests

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('Get the proxy: ', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self, page_count=2):
        '''Get proxies in kuaidaili.com
        
        args:
            page_count: max pages to search
        return:
            proxies
        '''
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling ', url)
            doc = pq(url)
            for item in doc('#list > table > tbody > tr').items():
                ip = item.find('td[data-title="IP"]').text().strip()
                port = item.find('td[data-title="PORT"]').text().strip()
                yield ':'.join([ip, port])
            time.sleep(1)

    def crawl_xicidaili(self, page_count=2):
        '''Get proxies in xicidaili.com
        
        args:
            page_count: max pages to search
        return:
            proxies
        '''
        start_url = 'https://www.xicidaili.com/nn/{}'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        for url in urls:
            print('Crawling ', url)
            doc = pq(url, headers=headers)
            for item in doc('#ip_list > tr[class]').items():
                ip = item.find('td:nth-child(2)').text()
                port = item.find('td:nth-child(3)').text()
                yield ':'.join([ip, port])
            time.sleep(1)
    
    def crawl_66ip(self, page_count=2):
        '''Get proxies in 66ip.cn
        
        args:
            page_count: max pages to search
        return:
            proxies
        '''
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling ', url)
            doc = pq(url)
            for item in doc('#main > div > div:nth-child(1) > table > tr:nth-child(n+2)').items():
                ip = item.find('td:nth-child(1)').text()
                port = item.find('td:nth-child(2)').text()
                yield ':'.join([ip, port])
            time.sleep(1)
    
    def crawl_ip3366(self, page_count=2):
        '''Get proxies in ip3366.net
        
        args:
            page_count: max pages to search
        return:
            proxies
        '''
        start_url = 'http://www.ip3366.net/free/?stype=1&page={}'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling ', url)
            doc = pq(url)
            for item in doc('#list > table > tbody > tr').items():
                ip = item.find('td:nth-child(1)').text()
                port = item.find('td:nth-child(2)').text() 
                yield ':'.join([ip, port])
            time.sleep(1)
   
    def crawl_goubanjia(self, page_count=1):
        '''Get proxies in goubanjia.com

        args:
            page_count: page refresh times
        return:
            proxies
        '''
        page = page_count
        while page > 0:
            url = 'http://www.goubanjia.com/'
            print('Crawling ', url, 'Time:', page_count - page + 1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }
            doc = pq(url, headers=headers)
            for item in doc('#services > div > div.row > div > div > div > table > tbody > tr').items():
                item = item.find('td.ip').remove('p')
                yield item.text().replace('\n', '')
            time.sleep(1)
            page -= 1


#if __name__ == "__main__":
#    crawl = Crawler()
#    for proxy in crawl.crawl_kuaidaili():
#    for proxy in crawl.crawl_xicidaili():
#    for proxy in crawl.crawl_66ip():
#    for proxy in crawl.crawl_goubanjia():
#    for proxy in crawl.crawl_ip3366():
#        print('proxy: ', proxy)