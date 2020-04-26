import requests

proxy = '60.190.250.120:8080'
proxies = {
    'http': proxy
}
try:
    req = requests.get('http://www.baidu.com', proxies=proxies, timeout=3)
    print(req.status_code)
    print()
#    print(req.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)