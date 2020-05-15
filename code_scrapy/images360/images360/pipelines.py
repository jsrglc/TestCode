# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy
from urllib.parse import urlparse

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.MongoDB_collection].insert_one(dict(item))
        return item
    
    def close_spider(self, spider):
        self.client.close()

class MySQLPipeline(object):
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_database):
        self.host = mysql_host
        self.user = mysql_user
        self.password = mysql_password
        self.database = mysql_database
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host = crawler.settings.get('MYSQL_HOST'),
            mysql_user = crawler.settings.get('MYSQL_USER'),
            mysql_password = crawler.settings.get('MYSQL_PASSWORD'),
            mysql_database = crawler.settings.get('MYSQL_DATABASE')
            )

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            charset = 'utf8'
        )
        self.cursor = self.conn.cursor()
    
    def process_item(self, item, spider):
        keys = ', '.join(dict(item).keys())
        strs = ', '.join(['%s'] * len(dict(item)))
        sql = 'INSERT INTO {}({}) VALUES ({})'.format(item.MySQL_table, keys, strs)
        self.cursor.execute(sql, list(dict(item).values()))
        self.conn.commit()        
        return item

    def close_spider(self, spider):
        self.conn.close()

class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        filename = urlparse(request.url).path.split('/')[-1]
        return filename

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no files")
        return item