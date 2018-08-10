import json
import os
import sys
import pickle
from datetime import datetime
from bson.json_util import dumps
import redis

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))
import database_client
import recommender_system_client
from message_client import MessageClient

REDIS_HOST = "localhost"
REDIS_PORT = 6379

NEWS_TABLE_NAME = "news"

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECONDS = 600
LOG_CLICKS_QUEUE_URL = "amqp://ntdtrqcd:4TupPgKPGYmsUZcT4SiO4PNAE9hvD1fo@emu.rmq.cloudamqp.com/ntdtrqcd"
LOG_CLICKS_QUEUE_NAME = "logs"

message_client = MessageClient(LOG_CLICKS_QUEUE_URL, LOG_CLICKS_QUEUE_NAME)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    if redis_client.get(user_id) is not None:
        total_news_digests = pickle.loads(redis_client.get(user_id))

        sliced_news_digests = total_news_digests[begin_index:end_index]
        db = database_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        db = database_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = [x['digest'] for x in total_news]

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index: end_index]


    # Get preference for the user.
    preference = recommender_system_client.getPreferenceForUser(user_id)
    topPrefence = None
    print ('top preference %s' % topPrefence)

    if preference is not None and len(preference) > 0:
        topPrefence = preference[0]
        print ('top preference %s' % topPrefence)

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
        if news['class'] == topPrefence:
            news['reason'] = "Recommend"
    result = json.loads(dumps(sliced_news))
    # print result
    return result

def recordClickLogForUser(user_id, news_id):
    print ('send click message!!!')
    message_for_queue = {'user_id': user_id, 'news_id': news_id, 'timestamp': str(datetime.utcnow())}
    print (message_for_queue)
    message_client.sendMessage(message_for_queue)

