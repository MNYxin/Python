# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    #大类标题和url
    parentTitle = scrapy.Field()
    parentUrl = scrapy.Field()

    # 小类标题和url
    subTitle = scrapy.Field()
    subUrl = scrapy.Field()
    subFileName = scrapy.Field()

    # 文章标题、连接、时间、内容
    name = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()

