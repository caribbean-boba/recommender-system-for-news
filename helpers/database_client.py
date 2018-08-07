from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017
DB = 'news'

client = MongoClient("%s:%d" % (HOST, PORT))

def get_db(db=DB):
    db = client[db]
    return db

