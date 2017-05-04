# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random
from settings import USER_AGENT_LIST


class RandomUserAgent(obejct):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers.setdefault('User-Agent': user_agent)
