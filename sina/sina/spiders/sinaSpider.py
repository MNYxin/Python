# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import SinaItem
from ..settings import Parent_File_Name

class SinaspiderSpider(scrapy.Spider):
    name = 'sinaSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 大类标题和url
        parentTitle = response.xpath('//h3[@class="tit02"]/a/text()').extract()
        parentUrls = response.xpath('//h3[@class="tit02"]/a/@href').extract()
        #print(parentUrls)

        # 小类标题和url
        subTitle = response.xpath('//ul[@class="list01"]/li/a/text()').extract()
        subUrls = response.xpath('//ul[@class="list01"]/li/a/@href').extract()
        #print(subUrls[0])

        # 爬取所有大类
        for i in range(0, len(parentTitle)):
            # 爬取所有小类
            for j in range(0, len(subTitle)):
                item = SinaItem()

                # 保存大类的title和urls
                item['parentTitle'] = parentTitle[i]
                item['parentUrl'] = parentUrls[i]

                # 检查小类的url是否以同类别大类url开头，如果是返回True (sports.sina.com.cn 和 sports.sina.com.cn/nba)
                if_belong = subUrls[j].startswith(item['parentUrl'])

                if(if_belong):

                    subFileName = Parent_File_Name + '/' +parentTitle[i] + '/' +subTitle[j]

                    # 如果目录不存在，则创建目录
                    if (not os.path.exists(subFileName)):
                        os.makedirs(subFileName)

                    # 存储 小类url、title和filename字段数据
                    item['subUrl'] = subUrls[j]
                    item['subTitle'] = subTitle[j]
                    item['subFileName'] = subFileName

                    #爬取每个小类中的数据
                    yield scrapy.Request(url = subUrls[j], meta = {'meta_1' : item}, callback = self.second_parse)

    def second_parse(self, response):
        #提取每次response的meta
        meta_1 = response.meta['meta_1']

        #文章url
        url = response.xpath('//a/@href').extract()

        for i in range(0, len(url)):
            # 检查每个链接是否以大类url开头、以.shtml结尾，如果是返回True
            if_belong = url[i].endswith('.shtml') and url[i].startswith(meta_1['parentUrl'])

            # 如果属于本大类，获取字段值放在同一个item下便于传输
            if (if_belong):
                item = SinaItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrl'] = meta_1['parentUrl']
                item['subUrl'] = meta_1['subUrl']
                item['subTitle'] = meta_1['subTitle']
                item['subFileName'] = meta_1['subFileName']
                item['url'] = url[i]
                #print(url[i])
                # 发送每个小类下子链接url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理
                yield scrapy.Request(url = url[i], meta = {'meta_2': item}, callback = self.detail_parse)

    def detail_parse(self, response):
        #提取每次response的meta
        item = response.meta['meta_2']
        content = ""

        #文章url
        name = response.xpath('//h1[@class="main-title"]/text()').extract()[0]
        time = response.xpath('//span[@class="date"]/text()').extract()[0]
        content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()
        #print(name)

        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one

        item['name'] = name
        item['time'] = time
        item['content'] = content

        yield item
