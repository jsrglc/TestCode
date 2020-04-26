from urllib.parse import urlencode
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests, re

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Referer': 'https://m.weibo.cn/u/2830678474',
        'X-Requested-With': 'XMLHttpRequest'
        }
    req = requests.get(url, headers=headers)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    return req.json()

def parse_page(json):
    weibos = []
    if json:
        items = json.get('data').get('cards')
        for item in items:
            weibo = {}
            weibo['id'] = item.get('mblog').get('id')

            weibo['text'] = re.sub(r'<.*?>', '', item.get('mblog').get('text'), flags=re.S)
            if '全文' in weibo['text']:
                detail_url = 'https://m.weibo.cn/statuses/extend?id=' + weibo['id']
                weibo['text'] = get_page(detail_url).get('data').get('longTextContent').replace('<br />', '')
            
            weibo['created_at'] = item.get('mblog').get('created_at')
            weibo['edit_at'] = item.get('mblog').get('edit_at')
            weibo['attitudes'] = item.get('mblog').get('attitudes_count')
            weibo['comments'] = item.get('mblog').get('comments_count')
            weibo['reposts'] = item.get('mblog').get('reposts_count')
            weibos.append(weibo)
    return weibos

#def save_to_mongo(result):
#    if collection.insert_one(result):
#        print('Saved to Mongo!')

if __name__ == "__main__":
    collection = MongoClient().weibo.weibo
    
    since_id = '0'
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474'
        }
    while since_id:        
        if since_id != '0':
            params['since_id'] = since_id

        url = 'https://m.weibo.cn/api/container/getIndex?' + urlencode(params)
        json = get_page(url)

        results = parse_page(json)
        for result in results:
            collection.insert_one(result)
#            print(result)
        since_id = json.get('data').get('cardlistInfo').get('since_id')
        print('Printed length:{} since_id: {}'.format(len(results), since_id))