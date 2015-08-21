# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()

    datetime = scrapy.Field()
    
    views_count = scrapy.Field()
    comments_count = scrapy.Field()
    likes_count = scrapy.Field()
    wordnum = scrapy.Field()

    followers_count = scrapy.Field()
    total_likes_count = scrapy.Field()
    # rank字段是文章评分，根据评分rank大小，对文章数据做持久化处理
    rank = scrapy.Field()


