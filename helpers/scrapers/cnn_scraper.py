import os
import random
import requests

from lxml import html

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []
GET_CNN_NEWS_XPATH = """//div[contains(@class, 'zn-body__paragraph')]//text() | //p[contains(@class, 'zn-body__paragraph')]//text()"""

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1: -1])
random.shuffle(USER_AGENTS)


def extract_news(news_url):
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=getHeaders())

    news = {}

    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        print # coding=utf-8
        return {}

    return news

def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection": "close",
        "user-Agent": ua
    }
    return headers