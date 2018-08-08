import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_scraper
from message_client import MessageClient
# pip install git+https://github.com/codelucas/newspaper.git@python-2-head
from newspaper import Article

DEDUPE_QUEUE_URL = "amqp://lqtrezfw:6JwRwmAPuMAMLdCnsCTrhVjO0W799DjK@lion.rmq.cloudamqp.com/lqtrezfw"
DEDUPE_QUEUE_NAME = "dedup-news-task"
SCRAPE_QUEUE_URL = "amqp://pcmwjrjr:Ztb_W2cjJF5AJqyYTLzU0e5tzvcCxnd8@lion.rmq.cloudamqp.com/pcmwjrjr"
SCRAPE_QUEUE_NAME = "scrape-news-task"

dedupe_client = MessageClient(DEDUPE_QUEUE_URL, DEDUPE_QUEUE_NAME)
scrape_client = MessageClient(SCRAPE_QUEUE_URL, SCRAPE_QUEUE_NAME)


def process_message(msg):
    task = msg
    text = None
    # print task['url']
    # source = task['source']
    # if source['id'] == 'cnn':
    #     text = cnn_scraper.extract_news(task['url'])
    # else:
    #     print task['source']
    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text

    dedupe_client.sendMessage(task)

while True:
    if scrape_client is not None:
        msg = scrape_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                process_message(msg)
            except Exception as e:
                print(e)
                pass
        scrape_client.sleep(5)