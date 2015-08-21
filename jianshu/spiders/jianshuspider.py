# __author__ = 'admin'
# -*- coding:utf-8 -*-

from jianshu.items import JianshuItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log


class JianshuSpider(CrawlSpider):
    name = 'JSSpider'
    start_urls = ['http://www.jianshu.com/', ]
    allowed_domains = ['jianshu.com']
    # url抓取规则
    # 第一个Rule规则对象定义抓取URL的来源
    # 第二个URL规则对象表示从上面的Rule抓取的页面中抓取URL
    rules = (
        Rule(LinkExtractor(allow=('/collection/', ), deny=('/users/', '/collections/'), unique=True), follow=True),
        Rule(LinkExtractor(allow=('/p/(.*)+', ), unique=True), callback='parse_item', follow=True),
    )

    # 运用合同（contract）对spider做测试, 查看items是否正常
    # 命令行执行：scarpy check JSSpider
    def parse_item(self, response):
        """ This function parses a sample response. Some contracts are mingled
        with this docstring.

        @url http://www.jianshu.com/p/b851e04de659
        @returns items 1 16
        @scrapes  author content title url datetime wordnum views_count
        comments_count likes_count followers_count total_likes_count rank
        """

        item = JianshuItem()
        log.start(logfile='log.txt', loglevel=log.INFO)
        log.msg('RequestURL:%s' % response.url, spider=JSSpider)
        contents = response.xpath('//div[contains(@class, "preview")]')[0]
        item['title'] = contents.xpath('h1[contains(@class,"title")]/text()').extract()[0]
        item['author'] = contents.xpath('div/a[contains(@class,"author-name")]/span/text()').extract()[0]
        item['datetime'] = contents.xpath('div[contains(@class,"author-info")]/span/text()').extract()[1]
        pagecons = response.xpath('//div[contains(@class, "show-content")]/p')
        item['content'] = pagecons.extract()
        item['url'] = response.url
        scriptlists = response.xpath('//script[contains(@data-name,"note")]/text()').extract()
        scriptlist6 = scriptlists[0].strip().split(',')[-6:]
        newscripts = []
        for script in scriptlist6:
            newscripts += script.encode('utf8').split(':')
        newscript = [n.replace('"', '') for n in newscripts]
        newdict = dict(newscript[i:i+2] for i in range(0, len(newscript), 2))
        item['wordnum'] = newdict.get('wordage')
        item['views_count'] = newdict.get('views_count')
        item['likes_count'] = newdict.get('likes_count')
        item['comments_count'] = newdict.get('comments_count')
        followersandtotallikes = response.xpath('//script[contains(@data-name,"author")]/text()').extract()
        followersandtotallikes2 = followersandtotallikes[0].strip().split(',')[-3:-1]
        newfollowersandtotallikes2 = []
        for followersandlikes in followersandtotallikes2:
            newfollowersandtotallikes2 += followersandlikes.encode('utf8').split(':')
        followerslikes = [n.replace('"', '') for n in newfollowersandtotallikes2]
        followerslikesdict = dict(followerslikes[i:i+2] for i in range(0, len(followerslikes), 2))
        item['followers_count'] = followerslikesdict.get('followers_count')
        item['total_likes_count'] = followerslikesdict.get('total_likes_count')
        return item

JSSpider = JianshuSpider()
