import requests
from urllib.parse import quote
url = 'http://192.168.99.102:8050/execute?lua_source='
lua_source = '''
function main(splash, args)
    splash:go('http://httpbin.org/get')
    return {
        html=splash:html()
        }
end
'''
url = url + quote(lua_source)
response = requests.get(url)
print(response.text)