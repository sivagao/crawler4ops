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
from scrapy.exceptions import DropItem

connection = Connection('localhost', 27017) # the default is 27017
db_user = connection.tbusers
db_thread = connection.tbthreads
db_wbuserstatus = connection.wbuserstatus
# db_user['modules'].remove({}) #temporary hack - delete all records

class TiebaPipeline(object):

    def __init__(self):
        self.wbuserstatus_sid_seen = set()

    def process_item(self, item, spider):
        """
            For each item, insert into mongodb as dict
        """
        alias = urllib.unquote(spider.alias).decode('gb2312')
        if spider.name == 'tb_user':
            db_user[alias].insert(dict(item))
        elif spider.name == 'tb_thread':
            db_thread[alias].insert(dict(item))
        elif spider.name == 'wb_userstatus':
            if item.get('pdate','') in self.wbuserstatus_sid_seen:
                raise DropItem("Duplicate item found: %s" % item)
            elif item.get('text', '') == '':
                raise DropItem("Empty item found: %s" % item)
            else:
                self.wbuserstatus_sid_seen.add(item['pdate'])
                db_wbuserstatus[alias].insert(dict(item))
        return item
