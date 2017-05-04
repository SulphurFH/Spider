# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from doubanCrawlSpider.items import DoubancrawlspiderItem


class DoubanSpider(CrawlSpider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']

    page_links = LinkExtractor(allow=('\?start=\d+&filter='))

    rules = [
        Rule(page_links, callback='page_parse', follow=True)
    ]

    def page_parse(self, response):
        item = DoubancrawlspiderItem()
        movieInfo = response.xpath('//div[@class="info"]')
        for movie in movieInfo:
            item['title'] = movie.xpath(
                './div[@class="hd"]/a/span[@class="title"]/text()')[0].extract()
            item['score'] = movie.xpath(
                './div[@class="bd"]/div[@class="star"]/span/text()')[0].extract()
            content = movie.xpath('./div[@class="bd"]/p/text()')
            item['content'] = content[0].extract().strip() if len(
                content) > 0 else 'NULL'
            info = movie.xpath(
                './div[@class="bd"]/p[@class="quote"]/span/text()')
            item['info'] = info[0].extract() if len(info) > 0 else 'NULL'

            yield item
