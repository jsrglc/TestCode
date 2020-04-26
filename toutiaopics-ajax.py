from urllib.parse import urlencode
from multiprocessing.pool import Pool 
import requests, os

def get_json(url):
    headers = {
        'cookie': 'tt_webid=6796818188640470536; ttcid=4612744176fd439eb20e45c0c9f7dc6b23; csrftoken=fc3ec833e914fb91a263dca31f398826; tt_webid=6796818188640470536; s_v_web_id=verify_k8gzzpja_DmYWnWPY_tCRh_46Hl_At5k_mqYojAAXQeUb; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=wci0f5b811585725456454; SLARDAR_WEB_ID=ce1626fe-002e-45ba-b74f-934ac08ecd47; tt_scid=EjYY1nDZgRDl3UWk46XZlSCFhWnV0k2KL20MGqmlY4jpMUbqLxq0TEUyWz-6k6wAc237',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    req = requests.get(url, headers=headers)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    return req.json()

def save_pic(url,dirname):
    name_pic = dirname + '/' + url.split('/')[-1] + '.jpg'
    url = url.replace('list', 'origin')
    req = requests.get(url)
    if req.status_code != 200:
        url = url.replace('origin', 'large')
        req = requests.get(url)
        if req.status_code != 200:
            url = url.replace('large', 'list')
            req = requests.get(url)
    content = req.content
    with open(name_pic, 'wb') as f:
        f.write(content)

def parse_data(offset):
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20'
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    items = get_json(url).get('data')
    for item in items:
        dirname = item.get('title')
        #.replace('/','').replace('\','').replace(':','').replace('*','').replace('"','').replace('<','').replace('>','').replace('|','').replace('?','')
        image_list = item.get('image_list')
        if image_list and dirname:
            if len(dirname) > 10:
                dirname = dirname[:10]
            dirname = 'pics/' + dirname
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            for image in image_list:
                image_url = image.get('url')
                save_pic(image_url, dirname)
            print('printing offset:{}  title:{}  pics:{}'.format(offset, dirname[5:],len(image_list)))

if __name__ == "__main__":
#    pool = Pool()
#    group = [i*20 for i in range(3)]
#    pool.map(parse_data, group)
#    pool.close()
#   pool.join()
    parse_data(0)
    parse_data(20)
    parse_data(40)
