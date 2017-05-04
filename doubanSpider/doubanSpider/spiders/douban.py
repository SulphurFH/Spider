# -*- coding: utf-8 -*-
import scrapy
from doubanSpider.items import DoubanspiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    url = 'https://movie.douban.com/top250?start='
    offset = 0
    end = '&filter='
    start_urls = [url + str(offset) + end]

    def parse(self, response):
        item = DoubanspiderItem()
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

        if self.offset <= 225:
            self.offset += 25
            url = self.url + str(self.offset) + self.end
            yield scrapy.Request(url, callback=self.parse)
