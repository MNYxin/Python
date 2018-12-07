# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import SisItem

class SisspiderSpider(scrapy.Spider):
    name = 'sisSpider'
    allowed_domains = ['38.103.161.131']
    start_urls = ['http://38.103.161.131/forum/forumdisplay.php?fid=25&filter=type&typeid=76&page=1']
    max_page = 30

    def parse(self, response):
        # 明细url
        detail_url_list = response.xpath("//tbody/tr/th/span/a/@href").extract()
        for detail_url in detail_url_list:
            detail_url ='http://38.103.161.131/forum/'+detail_url
            time.sleep(2)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)
        cur_page_num = int(response.url.split('&page=')[1])
        next_page_num = cur_page_num + 1
        if cur_page_num < self.max_page:
            next_url = response.url[:-len(str(cur_page_num))] + str(next_page_num)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        item = SisItem()
        # 名字
        name = response.xpath("//div[@class='postmessage defaultpost']/h2/text()").extract()[0]
        name = name.replace('.', '').replace('\\', '').replace('/', '').replace(' ', '').replace(':', '').replace('*','').replace('"', '')
        item['name'] = name
        print(name)
        # 时间
        item['time'] = response.xpath("//div[@class='postinfo']/text()[5]").extract()[0].split(' ')[1]
        print(item['time'])
        # 图片
        item['image_urls'] = response.xpath("//div[@class='mainbox viewthread'][1]//div[@class='postmessage defaultpost']/div//img/@src").extract()
        #print(item['image_urls'])
        # 内容
        #item['content'] = response.xpath("//div[@class='postmessage defaultpost']/h2/text()").extract()[0]
        # 种子
        item['file_urls'] = 'http://38.103.161.131/forum/' + response.xpath("//dl[@class='t_attachlist']/dt/a[2]/@href").extract()[0]
        #print(item['torrent_url'])
        yield item