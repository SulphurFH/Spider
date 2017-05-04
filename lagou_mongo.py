# coding=utf-8
import requests
import threading
from lxml import etree
from pymongo import *
from time import time, sleep


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
}

proxies = {
    'http': '124.88.67.19:80'
}


def loadSpider(startPage, endPage):
    # searchName = raw_input('请输入要爬取的名称:')
    searchName = 'Python'
    # startPage = 1
    # endPage = 30

    for pageNum in range(startPage, endPage + 1):
        url = 'https://www.lagou.com/zhaopin/' + searchName + \
              '/' + str(pageNum) + '/?filterOption=3'
        print url
        sleep(3)
        req = requests.get(url, headers=headers, proxies=proxies)

        loadPage(req.text.encode('UTF-8'))


def loadPage(response):
    selector = etree.HTML(response)
    jobLinks = selector.xpath('//a[@class="position_link"]/@href')

    for link in jobLinks:
        print link
        sleep(3)
        rep = requests.get(link, headers=headers, proxies=proxies)
        getData(rep.text.encode('UTF-8'))


def getData(response):
    selector = etree.HTML(response)
    campanyName = ' '.join(selector.xpath(
        '//div[@class="company"]/text()'))
    print campanyName
    salary = ' '.join(selector.xpath(
        '//span[@class="salary"]/text()'))
    localtion = ' '.join(selector.xpath(
        '//div[@class="work_addr"]/a/text()'))
    exprience = ' '.join(selector.xpath(
        '//dd[@class="job_request"]/p/span[3]/text()')).replace(' ', '').replace('/', '')
    academic = ' '.join(selector.xpath(
        '//dd[@class="job_request"]/p/span[4]/text()')).replace(' ', '').replace('/', '')
    jobType = ' '.join(selector.xpath(
        '//dd[@class="job_request"]/p/span[5]/text()')).replace(' ', '').replace('/', '')
    advantage = ' '.join(selector.xpath(
        '//dd[@class="job-advantage"]/p/text()'))
    jobBt = ' '.join(selector.xpath(
        '//dd[@class="job_bt"]//p/text()'))

    joblists = {'campanyName': campanyName, 'salary': salary, 'localtion': localtion, 'exprience': exprience,
                'academic': academic, 'jobType': jobType, 'advantage': advantage, 'jobBt': jobBt}
    # print joblists
    insertMongo(joblists)


def insertMongo(joblists):
    client = MongoClient('192.168.0.103', 27017)
    db = client.lagou
    collection = db.Python
    collection.insert_one(joblists)


if __name__ == '__main__':
    startTime = time()
    print startTime
    startPage = 1
    endPage = 10
    for _ in range(3):
        t = threading.Thread(target=loadSpider, args=(startPage, endPage))
        t.start()
        startPage += 10
        endPage += 10
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    # loadSpider(1, 30)
    endTime = time()
    print endTime

    print 'Using {}s'.format(endTime - startTime)
