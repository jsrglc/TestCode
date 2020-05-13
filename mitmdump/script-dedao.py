from mitmproxy import ctx
import json, pymongo

client = pymongo.MongoClient()
collection = client.igetget.books

def response(flow):
    url = 'https://entree.igetget.com/label/navigation/content'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        for book in books:
            data = {
                'title': book.get('name'),
                'author': book.get('author_list'),
                'cover': book.get('index_img'),
                'summary': book.get('intro'),
                'price': book.get('price')
            }
            ctx.log.info(str(data))
            collection.insert_one(data)