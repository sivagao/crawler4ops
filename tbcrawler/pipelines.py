# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from pymongo import Connection
import urllib

connection = Connection('localhost', 27017) # the default is 27017
db = connection.tbusers
db['modules'].remove({}) #temporary hack - delete all records

class TiebaPipeline(object):
    def process_item(self, item, spider):
        """For each item, insert into mongodb as dict
        """
        alias = urllib.unquote(spider.alias).decode('gb2312')
        db[alias].insert(dict(item))
        return item
