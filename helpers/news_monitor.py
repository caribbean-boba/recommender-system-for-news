
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
NEWS_SOURCES = 'cnn, bbc-news, bbc-sport, bloomberg,cnn, entertainment-weekly,espn, the-new-york-times,techcrunch, the-washington-post,the-wall-street-journal, espn'
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
message_client = MessageClient(MESSAGE_QUEUE_URL, MESSAGE_QUEUE_NAME)

while True:
    news_list = newsapi_client.getNews(NEWS_SOURCES)
    # print NEWS_SOURCES
    # print news_list
    count_new_news = 0
    for news in news_list:
        # user sha256 to generate digest
        news_digest = hashlib.sha256(news['title'].encode('UTF-8')).digest().encode('base64')
        if redis_client.get(news_digest) is None:
            news['digest'] = news_digest
            count_new_news += 1
            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            redis_client.set(news_digest, news)
            # two day = 3600 * 48
            redis_client.expire(news_digest, 3600 * 48)
            message_client.sendMessage(news)

    print "Get %d news" % count_new_news

    message_client.sleep(5)


