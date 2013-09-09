# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TbUser(Item):
    name = Field()

class TbThread(Item):
    title = Field()
    url = Field()
    postnum = Field()

class WbUserstatus(Item):
    """
    text, url, retweetnum, commentnum, pdate, favonum
    """
    sid = Field()
    text = Field()
    url = Field()
    retweetnum = Field()
    commentnum = Field()
    pdate = Field()
    favonum = Field()
