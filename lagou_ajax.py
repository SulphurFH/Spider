# coding=utf-8
import requests
import threading
from Queue import Queue
import time
import json

dataQueue = Queue()
exitFlag_Parser = False


class CrawlThread(threading.Thread):
    def __init__(self, threadName, pageQueue, spiderName):
        super(CrawlThread, self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.url = 'http://www.lagou.com/jobs/positionAjax.json?city='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        }
        self.proxies = {
            'http': '124.88.67.19:80'
        }
        self.cookies = {
            'LGUID': '20170411121621-9e375938-1e6d-11e7-84ec-525400f775ce',
        }
        self.spiderName = spiderName

    def run(self):
        # print 'Crawl{}采集开始'.format(self.threadName)
        while True:
            if self.pageQueue.empty():
                break
            else:
                url = self.url + self.spiderName + '&needAddtionalResult=false'
                try:
                    pn = self.pageQueue.get(False)
                except:
                    pass
                data = {
                    'first': True,
                    'pn': pn,
                    'kd': self.spiderName
                }
                # print data
                req = requests.post(url, headers=self.headers, cookies=self.cookies,
                                    proxies=self.proxies, data=data)
                print req.content
                dataQueue.put(req.content)


class ParserThread(threading.Thread):
    def __init__(self, threadName, dataQueue):
        super(ParserThread, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue

    def run(self):
        while not exitFlag_Parser:
            try:
                content = json.loads(self.dataQueue.get(False))
            except:
                pass
            # content = json.loads(self.dataQueue.get(False))
            print content['content']['positionResult']['result']
            # print '{}结束'.format(self.threadName)
        # print 'Ending'


def main():
    spiderName = raw_input('请输入爬取得名称：')
    pageNum = int(raw_input('请输入爬取得页数：'))
    pageQueue = Queue(pageNum)

    for page in range(1, pageNum + 1):
        pageQueue.put(page)

    crawlThreadList = []
    for t in range(3):
        thread = CrawlThread(t, pageQueue, spiderName)
        thread.start()
        crawlThreadList.append(thread)

    for t in crawlThreadList:
        t.join()

    parserthreadList = []
    for t in range(3):
        thread = ParserThread(t, dataQueue)
        thread.start()
        parserthreadList.append(thread)
        # print dataQueue.qsize()

    global exitFlag_Parser
    while not dataQueue.empty():
        pass
    exitFlag_Parser = True

    for t in parserthreadList:
        t.join()


if __name__ == '__main__':
    main()
