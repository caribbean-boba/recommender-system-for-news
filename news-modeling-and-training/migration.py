import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))

import database_client
import model_server_client

if __name__ == '__main__':
    db = database_client.get_db()
    cursor = db['news'].find({})
    count = 0
    for news in cursor:
        count += 1
        print(count)
        
        if 'class' not in news:
            print('Populating classes...')
            description = news['description']
            if description is None:
                description = news['title']
            news['class'] = model_server_client.classify(description)
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)