
dic = {
  "item": {
    "class": "NewsItem",
    "attrs": {
      "title": [
        {
          "method": "xpath",
          "args": [
            "text()"
          ]
        }
      ],
      "url": [
        {
          "method": "attr",
          "args": [
            "url1", "url2", "url3"
          ],
            "re": "来源：(.*)"
        }
      ],
    }
  }
}

for key, value in dic.get('item').get('attrs').items():
    print('value, ', value, '   ', type(value))
    print(value[0].get('method'))
    for ext in value:
        print(ext.get('method'))
        print(ext.get('args'))
        print(*ext.get('args'))
        print(ext.get('re'))
        print({'re': ext.get('re')})
        print(**{'dsd': ext.get('re')})
print('----')
'''
print(dic.get('item'))
print(type(dic.get('item')))
print(dic.get('item').get('class'))
print(type(dic.get('item').get('class')))
print(dic.get('item').get('attrs'))
print(type(dic.get('item').get('attrs')))
print(dic.get('item').get('attrs').get('title'))
print(type(dic.get('item').get('attrs').get('title')))
print(dic.get('item').get('attrs').get('title').get('method'))
print(type(dic.get('item').get('attrs').get('title').get('method')))
'''