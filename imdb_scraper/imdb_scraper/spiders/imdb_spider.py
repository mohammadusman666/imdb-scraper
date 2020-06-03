# -*- coding: utf-8 -*-
import scrapy

class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/']

    def parse(self, response):
        pass
