import operations
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))
from message_client import MessageClient
LOG_CLICKS_QUEUE_URL = "amqp://ntdtrqcd:4TupPgKPGYmsUZcT4SiO4PNAE9hvD1fo@emu.rmq.cloudamqp.com/ntdtrqcd"
LOG_CLICKS_QUEUE_NAME = "logs"

message_client = MessageClient(LOG_CLICKS_QUEUE_URL, LOG_CLICKS_QUEUE_NAME)

def test_getNewsSummariesForUser_basic():
    news = operations.getNewsSummariesForUser('user', 1)
    assert len(news) > 0
    print('test_getNewsSummariesForUser_basic passed')

def test_getNewsSummariesForUser_pagination():
    news_page_1 = operations.getNewsSummariesForUser('user', 1)
    news_page_2 = operations.getNewsSummariesForUser('user', 2)

    assert len(news_page_1) > 0
    assert len(news_page_2) > 0

    digests_page_1_set = set([news['digest'] for news in news_page_1])
    digests_page_2_set = set([news['digest'] for news in news_page_2])

    assert len(digests_page_1_set.intersection(digests_page_2_set)) == 0

    print('test_getNewsSummariesForUser_pagination passed!')

def test_logNewsClickForUser_basic():
    operations.recordClickLogForUser('test', 'test_news')

    msg = message_client.getMessage()
    assert msg is not None
    assert msg['user_id'] == 'test'
    assert msg['news_id'] == 'test_news'
    assert msg['timestamp'] is not None

    print 'test_logNewsClicksForUser_basic passed!'

if __name__ == "__main__":
    test_getNewsSummariesForUser_basic()
    test_getNewsSummariesForUser_pagination()
    test_logNewsClickForUser_basic()