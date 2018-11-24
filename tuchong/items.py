# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuchongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author_url = scrapy.Field()  # 作者首页地址
    url = scrapy.Field()  # 作品地址
    pic_urls = scrapy.Field()   # 图片地址列表
    title = scrapy.Field()  # 标题
    img_count = scrapy.Field()  # 图片数
    published_time = scrapy.Field()  # 发布时间
    favorites = scrapy.Field()  # 喜欢数
    views = scrapy.Field()  # 阅读量
    tags = scrapy.Field()   # tag
    comments = scrapy.Field()  # 评论
