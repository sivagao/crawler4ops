
from tbcrawler.items import TbUser

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

# define crawler
class TbUserSpider(CrawlSpider):

  name = 'tb_user'
  allowed_domain = ['tieba.baidu.com']
  rules = (Rule(SgmlLinkExtractor(allow=(r'/f/like/manage/list\?kw=.*&pn=\d+',)), callback='parse_user', follow=True),)

  def __init__(self, target=None, *args, **kwargs):
    super(TbUserSpider, self).__init__(*args, **kwargs)
    self.alias = target
    self.start_urls = ['http://tieba.baidu.com/f/like/manage/list?kw=%s' % target]
    # http://tieba.baidu.com/f/like/manage/list?kw=android&pn=100000000
    # url_start = 'http://tieba.baidu.com/f/like/manage/list?kw=%s' % target
    # self.start_urls = [url_start+'&pn=%s' % pn for pn in range(1, 9400)]
    # link_extractor = r'/f/like/manage/list\?kw=%s&pn=\d+' % target
    self.rules = (Rule(SgmlLinkExtractor(allow=(r'/f/like/manage/list\?kw=.*&pn=\d+',)), callback='parse_user', follow=True),)

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
