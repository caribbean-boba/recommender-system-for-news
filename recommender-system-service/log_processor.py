# -*- coding: utf-8 -*-

'''
Time decay model:
If selected:
p = (1-α)p + α
If not:
p = (1-α)p
'''

import news_classes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))

import database_client
from message_client import MessageClient

CLASS = 8
# 1.0 not 1 here to calculate correctly
INITIAL_P = 1.0 / CLASS
ALPHA = 0.1

PREFERENCE_MODEL_TABLE = "user_preference_model"
NEWS_TABLE = "news"


LOG_CLICKS_QUEUE_URL = "amqp://ntdtrqcd:4TupPgKPGYmsUZcT4SiO4PNAE9hvD1fo@emu.rmq.cloudamqp.com/ntdtrqcd"
LOG_CLICKS_QUEUE_NAME = "logs"

message_client = MessageClient(LOG_CLICKS_QUEUE_URL, LOG_CLICKS_QUEUE_NAME)


def process_message(message):
    # print ('??????111')
    print (message)
    if ('user_id' not in message or 'news_id' not in message):
        print ('user_id or news_id is missing')
        return
    # print ('??????444')
    user_id = message['user_id']
    news_id = message['news_id']
    print (user_id)
    # find the user in user_preference_model collection
    db = database_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE].find_one({'user_id':user_id})
    # print ('??????444')
    # If there is no model for the user, create a new one
    if model is None:
        print("New model for new user: %s" % user_id)
        news_model = {'user_id' : user_id}
        preference = {}
        for i in news_classes.class_map:
            preference[i] = float(INITIAL_P)
        news_model['preference'] = preference
        model = news_model

    print("Update model for user: %s" % user_id)

    # TIME DECAY MODEL
    print ("Clicked news has news_id %s" % news_id)
    news = db[NEWS_TABLE].find_one({'digest': news_id})
    # print ("news!!!!!!!! %s" % news)
    if (news is None or
        'class' not in news or
        news['class'] not in news_classes.class_map):
        print("Can not process this news since class %s is not in the class map" % news['class'])
        return

    # Update the clicked one.
    click_class = news['class']
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    # Update the non-clicked classes.
    for i, prob in model['preference'].items():
        if not i == click_class:
            old_p = model['preference'][i]
            model['preference'][i] = float((1 - ALPHA) * old_p)

    db[PREFERENCE_MODEL_TABLE].replace_one({'user_id': user_id}, model, upsert=True)
    print ("Processing log success!!")


def run():
    while True:
        if message_client is not None:
            message = message_client.getMessage()
            if message is not None:
                try:
                    process_message(message)
                except Exception as e:
                    print(e)
                    pass

            message_client.sleep(3)


if __name__ == "__main__":
    run()