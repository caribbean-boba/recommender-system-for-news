import newsapi_client as client
from json import loads

def test_basic():
    news = client.getNews()
    # news = news[0]
    # print news['source']
    assert len(news) > 0
    news = client.getNews(source='bbc-news')
    assert len(news) > 0
    print 'passed'

if __name__ == "__main__":
    test_basic()