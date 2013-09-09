
from tbcrawler.items import TbThread

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

# define crawlerh
# scrapy crawl tb -a target=android -s LOG_FILE=scrapy_tb_android.log
# scrapy crawl tb_thread -a target=android -o data/android_threads.json -f json
class TbThreadSpider(CrawlSpider):

	name = 'tb_thread'
	allowed_domain = ['tieba.baidu.com']
	rules = (Rule(SgmlLinkExtractor(allow=(r'/f\?kw=.*&pn=\d+',)), callback='parse_thread', follow=True),)

	def __init__(self, target=None, *args, **kwargs):
		super(TbThreadSpider, self).__init__(*args, **kwargs)
		self.alias = target
		self.start_urls = ['http://tieba.baidu.com/f?kw=%s' % target]
		# http://tieba.baidu.com/f/like/manage/list?kw=android&pn=100000000
		# url_start = 'http://tieba.baidu.com/f/like/manage/list?kw=%s' % target
		# self.start_urls = [url_start+'&pn=%s' % pn for pn in range(1, 9400)]
		# link_extractor = r'/f/like/manage/list\?kw=%s&pn=\d+' % target
		self.rules = (Rule(SgmlLinkExtractor(allow=(r'/f\?kw=.*&pn=\d+',)), callback='parse_thread', follow=True),)

	def parse_thread(self, response):

		hxs = HtmlXPathSelector(response)
		# threads = hxs.select("/div[@class='j_thread_list']").extract()
		threads = hxs.select('//*[@id="thread_list"]/li[@class="j_thread_list clearfix"]')
		# console.log(users)
		items = []

		for t in threads:

			item = TbThread()
			item['postnum'] = int(t.select('.//*[@class="threadlist_rep_num"]/text()').extract()[0])
			item['title'] = t.select('.//*[@class="j_th_tit"]/text()').extract()[0]
			item['url'] = t.select('.//*[@class="j_th_tit"]/@href').extract()[0]
			items.append(item)

		return items
