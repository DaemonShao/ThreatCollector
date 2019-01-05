# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from ConfigParser import ConfigParser

import ThreatCollector.settings as setting


class ThreatcollectorPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        host = setting.MONGODB_HOST
        port = setting.MONGODB_PORT
        db_name = setting.MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)

        self.db = client[db_name]

    def process_item(self, item, spider):

        config = ConfigParser()
        config.read("scrapy.cfg")

        table = self.db[spider.name]

        if spider.name == "hosts-file":
            table.create_index("host_name")
            table.create_index("add_time", expireAfterSeconds=int(config.get(spider.name, "expire_time")))

        if spider.name == "blocklist-de":
            table.ensure_index("ip")
            table.create_index("add_time", expireAfterSeconds=int(config.get(spider.name, "expire_time")))

        quote_into = dict(item)
        table.insert(quote_into)
        return item
