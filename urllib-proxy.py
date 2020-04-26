from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy = '163.204.246.98:9999'
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
#opener = build_opener()
try:
    response = opener.open('http://www.baidu.com')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)