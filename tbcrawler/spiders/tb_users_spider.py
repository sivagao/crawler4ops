
from scrapy.spider import BaseSpider
from tbcrawler.items import TbUser

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

# define crawler
class TbUsersSpider(CrawlSpider):

  name = 'tb'
  allowed_domain = ['tieba.baidu.com']
  rules = (Rule(SgmlLinkExtractor(allow=(r'/f/like/manage/list\?kw=.*&pn=\d+',)), callback='parse_user', follow=True),)

  def __init__(self, target=None, *args, **kwargs):
    super(TbUsersSpider, self).__init__(*args, **kwargs)
    self.alias = target
    self.start_urls = ['http://tieba.baidu.com/f/like/manage/list?kw=%s' % target]
    # link_extractor = r'/f/like/manage/list\?kw=%s&pn=\d+' % target
    # self.rules = (Rule(SgmlLinkExtractor(allow=(r'/f/like/manage/list\?kw=.*&pn=\d+',)), callback='parse_user', follow=True),)

  def parse_user(self, response):

    hxs = HtmlXPathSelector(response)
    users = hxs.select("//div[@class='mli_user']/div[@class='mli_user_name']/a/text()").extract()
    # console.log(users)
    items = []

    for user in users:
        item = TbUser()
        item['name'] = user
        items.append(item)

    return items
