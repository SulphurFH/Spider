# coding=utf-8
import requests
from lxml import etree
import xlwt


def loadSpider():
    searchName = raw_input('请输入要爬取的名称:')
    startPage = 11
    endPage = 24

    rowNum = 0
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')

    proxies = {
        'http': '124.88.67.19:80'
    }

    for pageNum in range(startPage, endPage + 1):
        # pageNum = 1
        url = 'https://www.lagou.com/zhaopin/' + searchName + \
              '/' + str(pageNum) + '/?filterOption=' + str(pageNum)
        print url
        req = requests.get(url, proxies=proxies)

        rowNum = loadPage(req.content, rowNum, sheet)
        print rowNum
        # return req.content
    wbk.save('test1.xls')


def loadPage(response, rowNum, sheet):
    selector = etree.HTML(response)
    jobLinks = selector.xpath('//a[@class="position_link"]/@href')

    for link in jobLinks:
        rep = requests.get(link)
        wirtePage(rep.content, rowNum, sheet)
        rowNum += 1
    return rowNum


def wirtePage(response, rowNum, sheet):
    selector = etree.HTML(response)
    campanyName = ' '.join(selector.xpath(
        '//div[@class="company"]/text()'))
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

    joblists = [campanyName, salary, localtion,
                exprience, academic, jobType, advantage, jobBt]

    # wbk = xlwt.Workbook()
    # sheet = wbk.add_sheet('sheet 1')
    for colNum, context in enumerate(joblists):
        sheet.write(rowNum, colNum, context)
        print '行:' + str(rowNum) + ';列:' + str(colNum)
        print '*' * 30
    # wbk.save('test.xls')


if __name__ == '__main__':
    loadSpider()
    # loadPage(response)
