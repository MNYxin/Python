# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from .settings import IMAGES_STORE
from .settings import FILES_STORE


class SisImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info): #下载图片
        for image_url in item['image_urls']:
            yield Request(image_url,meta={'item':item, 'index':item['image_urls'].index(image_url)}) #添加meta是为了下面重命名文件名使用

    def file_path(self,request,response=None,info=None):
        print(request.url)
        item=request.meta['item'] #通过上面的meta传递过来item
        index=request.meta['index'] #通过上面的index传递过来列表中当前下载图片的下标
        image_guid = item['name']+str(index)+'.'+request.url.split('/')[-1].split('.')[-1]
        #图片下载目录
        filename = u'{0}\{1}\{2}\{3}'.format(IMAGES_STORE, item['time'], item['name'], image_guid)
        return filename


class SisFilesPipeline(FilesPipeline):
    def get_media_requests(self,item,info): #下载图片
        yield Request(item['file_urls'], meta={'item': item})  # 添加meta是为了下面重命名文件名使用

    def file_path(self,request,response=None,info=None):
        print(request.url)
        item=request.meta['item'] #通过上面的meta传递过来item
        image_guid = item['name']+'.torrent'
        #文件下载目录
        filename = u'{0}\{1}\{2}\{3}'.format(FILES_STORE, item['time'], item['name'], image_guid)
        return filename