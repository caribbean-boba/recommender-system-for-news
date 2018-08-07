
# -*- coding: utf-8 -*-
import os
import sys
import redis
import hashlib
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import newsapi_client
from message_client import MessageClient
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
MESSAGE_QUEUE_URL = "amqp://pcmwjrjr:Ztb_W2cjJF5AJqyYTLzU0e5tzvcCxnd8@lion.rmq.cloudamqp.com/pcmwjrjr"
MESSAGE_QUEUE_NAME = 'scrape-news-task'
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24
SLEEP_TIME_IN_SECONDS = 10

NEWS_SOURCES = ['cnn']
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
message_client = MessageClient(MESSAGE_QUEUE_URL, MESSAGE_QUEUE_NAME)

while True:
    news_list = newsapi_client.getNews(NEWS_SOURCES)
    count_new_news = 0
    for news in news_list:
        news_digest = hashlib.sha256(news['title'].encode('UTF-8')).digest().encode('base64')
        if redis_client.get(news_digest) is None:
            count_new_news += 1
            news['digest'] = news_digest
            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)
            message_client.sendMessage(news)

    print "new news %d" % count_new_news

    message_client.sleep(SLEEP_TIME_IN_SECONDS)


