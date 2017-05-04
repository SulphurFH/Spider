# coding=utf-8
import requests
import threading
from Queue import Queue
from pymongo import *


class CrawlThread(threading.Thread):
    def __init__(self, threadName, pageQueue, spiderName):
        super(CrawlThread, self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.url = 'http://www.lagou.com/jobs/positionAjax.json?'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        }
        self.proxies = {
            'http': '124.88.67.19:80'
        }
        self.cookies = {
            'LGUID': '20170411121621-9e375938-1e6d-11e7-84ec-525400f775ce'
        }
        self.spiderName = spiderName
        self.urlpatt = {
            'city': '北京',
            'needAddtionalResult': 'false'
        }

    def run(self):
        while True:
            if self.pageQueue.empty():
                break
            else:
                try:
                    pn = self.pageQueue.get(False)
                    if pn == '':
                        break
                    else:
                        pass
                except:
                    pass
                data = {
                    'first': True,
                    'pn': pn,
                    'kd': self.spiderName
                }
                print '{} Starting'.format(self.threadName)
                req = requests.post(self.url, headers=self.headers, cookies=self.cookies,
                                    proxies=self.proxies, data=data, params=self.urlpatt)
                content = req.json()
                for item in content["content"]["positionResult"]["result"]:
                    self.wirteData(item)

    def wirteData(self, item):
        client = MongoClient('192.168.12.28', 27017)
        db = client.lagou
        collection = db.get_collection('Python_ajax')
        collection.insert_one(item)


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


if __name__ == '__main__':
    main()
