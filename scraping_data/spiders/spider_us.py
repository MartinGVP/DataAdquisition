# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scraping_data.items import us_header, us_article
from scrapy.crawler import CrawlerProcess
import urllib

class spider_usSpider(scrapy.Spider):
    name = 'spider_us'
    item_count = 0
    allowed_domains = ['catalog.data.gov']
    start_urls = ['https://catalog.data.gov/']
    custom_settings = {
        'DEPTH_LIMIT': 3,
        'CLOSESPIDER_ITEMCOUNT': 40,
        'FEED_FORMAT':'json',
        'FEED_EXPORT_INDENT':'1',
        'FEED_URI':'file:C://Users//mgvelasquez//Desktop//tarea_da//project_scraping//feature_article-%(time)s.json',
    }
    
    def parse(self, response):
        for flink in response.css(".dataset-heading > a"):
            link = response.urljoin(flink.attrib.get('href'))
            title = response.urljoin(flink.attrib.get('class'))
            yield response.follow(link,callback=self.parse_detail, meta= {'link':link, 'title':title})
        next_page=response.css('.module .pagination li:last-child ::attr(href)').extract_first()
        if next_page is not None:
            next_page_link= response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
			
    def parse_detail(self, response):
        items = us_header()
        item = us_article()
        items["link"] = response.meta["link"]
        item["title"] = response.xpath('//*[@id="content"]/div[2]/div/article/section[1]/h1/text()').extract()
        item["paragraph"] = response.xpath('//*[@id="content"]/div[2]/div/article/section[1]/div[2]/p/text()').extract()

        items["body"] = item #dentro de body quiero que este el titulo y el parrafo
        return items
