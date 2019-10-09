# -*- coding: utf-8 -*-
import scrapy


class CitationSpider(scrapy.Spider):
    name = 'citation'
    allowed_domains = ['cnki.net']
    start_urls = ['http://cnki.net/']

    def parse(self, response):
        pass
