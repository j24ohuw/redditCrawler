# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
from scrapy.exceptions import DropItem



##
##class RedditcrawlerPipeline(object):
##    def process_item(self, item, spider):
##        return item
##
##class DuplicatesPipeline(object):
##    def __init__(self):
##        self.ids_seen = set()
##    def process_item(self, item, spider):
##        if item['link'] in self.ids_seen:
##            raise DropItem("Duplicate item found: %s" % item)
##        else:
##            self.ids_seen.add(item['link'])
##        return item

class MongoPipeline(object):
    collection_name = 'data_test1'
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')# 'items')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()
            
    def process_item(self, item, spider):
##        valid = True
##        for data in item:
##            if not data:
##                valid = False
##                raise DropItem("Missing {0}!".format(data))
        self.db[self.collection_name].insert(dict(item))
        logging.debug("Added to MongoDB database")
        return item
