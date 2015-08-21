# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from scrapy.exceptions import DropItem
import re


class JianshuPipeline(object):
    def process_item(self, item, spider):
        views = int(item['views_count'])
        comments = int(item['comments_count'])
        likes = int(item['likes_count'])
        # 三者按比例简单求和
        votes = views*2 + comments*3 + likes*5

        # wordnum = int(item['wordnum'])
        # followers_count = int(item['followers_count'])
        # total_likes_count = int(item['total_likes_count'])
        starttime = item['datetime']
        # 对文章编辑时间格式化
        parsedstarttime = self.timeparsed(starttime)
        # 对现在时间格式化
        now = datetime.now()
        pattern = '%Y-%m-%d %H:%M'
        nowpattern = now.strftime(pattern)
        parsednowpattern = self.timeparsed(nowpattern)
        totaldelta = parsednowpattern - parsedstarttime
        totalhours = totaldelta.seconds/3600 + 2

        # 公式是votes = （p-1）/(t+2)^1.8 的改版
        rank = (votes - 1)/(pow(totalhours, 1.8))
        item['rank'] = str(rank)
        # item['datetime'] = str(totalhours)
        # 这里rank具体大小，可根据抓取的结果继续优化
        if rank > 36:
            return item
        else:
            raise DropItem('Rank  less than 2', item)

    def timeparsed(self, time1):
        # 针对编辑时间中的‘*’
        # 如果文章是做过修改的，那么简书文章的时间会带有'*'标记，为与系统时间格式保持一致，这里对'*'用''做替换处理
        edittiempattern = re.compile(r'\*')
        datetimeresult = re.search(edittiempattern, time1)
        if datetimeresult:
            time1 = time1.replace('*', '')
        pattern = re.compile(r'\.')
        match = re.search(pattern, time1)
        if match:
            time1 = time1.replace('.', '-')
        pattern = '%Y-%m-%d %H:%M'
        timeparsed = datetime.strptime(time1, pattern)
        return timeparsed
