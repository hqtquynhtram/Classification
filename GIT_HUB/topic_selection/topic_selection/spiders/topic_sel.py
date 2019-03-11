# -*- coding: utf-8 -*-
import scrapy
from topic_selection.items import TopicSelectionItem
from time import sleep
from scrapy.loader import ItemLoader



class TopicSelSpider(scrapy.Spider):
    name = 'topic_sel'
    allowed_domains = ['math.kth.se']
    start_urls = ['http://www.math.kth.se/matstat/sem.html']

    def parse(self, response):
        
        lists=response.xpath('//li')
        for element in lists:
            l=ItemLoader(item=TopicSelectionItem(),sel=element)
            author=element.xpath('.//b//text()').extract_first()
            if author:
                author=author.strip()
            topic=element.xpath('.//i//text()').extract_first()
            if topic:
                topic=topic.strip()
            url=element.xpath('./a/@href').extract_first()
            if url:
                url=url.strip()

            l.add_value('author',author)
            l.add_value('topic',topic)
            l.add_value('url',url)
            yield l.load_item()
