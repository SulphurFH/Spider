# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubancrawlspiderItem(scrapy.Item):
    # 电影标题
    title = scrapy.Field()
    # 电影评分
    score = scrapy.Field()
    # 电影信息
    content = scrapy.Field()
    # 简介
    info = scrapy.Field()
