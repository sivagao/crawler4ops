#!/usr/bin/python
# -*- coding: utf-8 -*-

from tbcrawler.items import WbUserstatus

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

import re

# define crawlerh
# scrapy crawl tb -a target=android -s LOG_FILE=scrapy_tb_android.log
# scrapy crawl tb_thread -a target=android -o data/android_threads.json -f json
class WbUserstatusSpider(CrawlSpider):

    name = 'wb_userstatus'
    allowed_domain = ['weibo.cn']
    # /kaifulee?page=2&gsid=4u5328be1qGKOj34kWAe7ar4c28&st=098b
    # rules = (Rule(SgmlLinkExtractor(allow=(r'/.*\?page=\d+.*',)), callback='parse_page', follow=True),)

    def __init__(self, target=None, *args, **kwargs):
        super(WbUserstatusSpider, self).__init__(*args, **kwargs)
        self.alias = target
        self.s_url = 'http://weibo.cn/%s' % target
        self.start_urls = [self.s_url+'?gsid=4u5328be1qGKOj34kWAe7ar4c28&st=098b']
        # http://tieba.baidu.com/f/like/manage/list?kw=android&pn=100000000
        # url_start = 'http://tieba.baidu.com/f/like/manage/list?kw=%s' % target
        # self.start_urls = [url_start+'&pn=%s' % pn for pn in range(1, 9400)]
        # link_extractor = r'/f/like/manage/list\?kw=%s&pn=\d+' % target
        # self.rules = (Rule(SgmlLinkExtractor(allow=(r'/f\?kw=.*&pn=\d+',)), callback='parse_topic', follow=True),)
    def parse_start_url(self, response):
        hxs = HtmlXPathSelector(response)
        s = hxs.select('//*[@id="pagelist"]/form/div/text()').extract()[-1]
        r = re.compile(ur'\/(\d*)页')
        pages = int(r.search(s).group(1))
        for link in [self.s_url+'?page=%s&gsid=4u5328be1qGKOj34kWAe7ar4c28&st=098b' % p for p in range(0, pages)]:
            yield Request(link, callback=self.parse_page)
        # return self.parse_page(response)

    def parse_page(self, response):

        hxs = HtmlXPathSelector(response)
        # threads = hxs.select("/div[@class='j_thread_list']").extract()
        statuses = hxs.select('//*[@class="c"][@id]')
        # threads = hxs.select('//*[@id="thread_list"]/li[@class="j_thread_list clearfix"]')
        # console.log(users)
        items = []

        for s in statuses:
            try:
                item = WbUserstatus()
                # text, url, retweetnum, commentnum, pdate, favonum
                alltext = ''.join(s.select('.//text()').extract())
                if alltext == '':
                    break
                r_retweetnum = re.compile(ur'(?<!原文)转发\[(.*?)\]')
                r_commentnum = re.compile(ur'(?<!原文)评论\[(.*?)\]')
                # todo, fix it!
                r_favonum = re.compile(ur'赞\[(.*?)\]')
                item['sid'] = s.select('./@id').extract()[0]
                item['retweetnum'] = int(r_retweetnum.search(alltext).group(1))
                item['commentnum'] = int(r_commentnum.search(alltext).group(1))
                item['favonum'] = int(r_favonum.search(alltext).group(1))
                item['text'] = alltext
                item['pdate'] = s.select('.//span[@class="ct"]/text()').extract()[0]
            except:
                None

            items.append(item)

        return items
