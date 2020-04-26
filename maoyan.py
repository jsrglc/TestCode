import re, time, json
import requests

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    r = requests.get(url, headers=headers, timeout=3)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def parse_one_page(html):
    items = []
    pattern = re.compile('board-index-(\d+)".*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)

    result = re.findall(pattern, html)
    for item in result:
        items.append({'index': item[0],
                'image': 'http:' + item[1],
                'title': item[2],
                'actor': item[3].strip()[3:],
                'time': item[4].strip()[5:],
                'score': item[5] + item[6]
            })
    return items

def output_item(item):
#    print(item)
    with open('maoyan.dat', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n') # dict to str

if __name__ == "__main__":
    base_url = 'http://maoyan.com/board/4?offset='
    for off_url in range(0, 100, 10):
        url =  base_url + str(off_url)
        html = get_one_page(url)
        time.sleep(1)
        
        print('parsing {} - {} records... '.format(off_url + 1, off_url + 10))
        for it in parse_one_page(html):
            output_item(it)  # screen and file output