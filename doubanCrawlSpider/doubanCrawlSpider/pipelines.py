# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import *


class DoubancrawlspiderPipeline(object):
    def __init__(self):
        self.ip = '192.168.12.30'
        self.port = 27017

    def process_item(self, item, spider):
        client = MongoClient(self.ip, self.port)
        db = client.douban
        collection = db.get_collection('movie_top_250_crawl')
        collection.insert_one(dict(item))

        return item
