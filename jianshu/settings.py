# -*- coding: utf-8 -*-

# Scrapy settings for jianshu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jianshu'

SPIDER_MODULES = ['jianshu.spiders']
NEWSPIDER_MODULE = 'jianshu.spiders'
ITEM_PIPELINES = {
    'jianshu.pipelines.JianshuPipeline': 500,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'jianshu (+http://www.yourdomain.com)'
