# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SisItem(scrapy.Item):
    # define the fields for your item here like:
    #名字
    name = scrapy.Field()
    #时间
    time = scrapy.Field()
    #图片
    image_urls = scrapy.Field()
    #内容
    content = scrapy.Field()
    # 种子
    file_urls = scrapy.Field()
