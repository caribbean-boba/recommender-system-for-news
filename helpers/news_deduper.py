import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

import database_client as db_client
from message_client import MessageClient

DEDUPE_QUEUE_URL = "amqp://lqtrezfw:6JwRwmAPuMAMLdCnsCTrhVjO0W799DjK@lion.rmq.cloudamqp.com/lqtrezfw"
DEDUPT_QUEUE_NAME = "dedup-news-task"

NEWS_TABLE_NAME = "news"

message_client = MessageClient(DEDUPE_QUEUE_URL, DEDUPT_QUEUE_NAME)

def process_message(msg):
    task = msg
    text = task['text']
    if text is None:
        return

    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = db_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print(pairwise_sim.A)

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            # similarity is 0.8
            if pairwise_sim[row, 0] > 0.8:
                print("Ignore duplicated news")
                return
    task['publishedAt'] = parser.parse(task['publishedAt'])

    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if message_client is not None:
        msg = message_client.getMessage()
        if msg is not None:
            try:
                process_message(msg)
            except Exception as e:
                print(e)
                pass

        message_client.sleep(5)