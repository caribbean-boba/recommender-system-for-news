

import numpy as np
import os
import pandas as pd
import pickle
import sys
import tensorflow as tf
import time

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import cnn_model

learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = './model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

N_CLASSES = 8

VARS_FILE = './vars'
VOCAB_PROCESSOR_SAVE_FILE = './vocab_procesor_save_file'

n_words = 0

MAX_DOCUMENT_LENGTH = 500
vocab_processor = None

classifier = None

class_map = {
  '1' : "World",
  '2' : "U.S.",
  '3' : "Business",
  '4' : "Technology",
  '5' : "Entertainment",
  '6' : "Sports",
  '7' : "Health",
  '8' : "Crime"
}
def restoreVars():
    with open(VARS_FILE, 'rb') as f:
        global n_words
        n_words = pickle.load(f)

    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
        VOCAB_PROCESSOR_SAVE_FILE)


def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)
    # Load data
    df = pd.read_csv('./labeled_news.csv', header=None)

    # tensorflow's bug. Need to call it to set all the parameters correctly
    train_df = df[0:400]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)

    print("Model update success.")


restoreVars()
loadModel()

print("Model loaded success.")


class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print("Reloading Model!")
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        retoreVars()
        loadModel()


observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()


def classify(text):
    text_series = pd.Series([text])
    predict_x = np.array(list(vocab_processor.transform(text_series)))
    print(predict_x)

    y_predicted = [
        p['class'] for p in classifier.predict(
            predict_x, as_iterable=True)
    ]
    print(y_predicted[0])
    topic = class_map[str(y_predicted[0])]
    return topic


RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')

print "Starting HTTP server ..."
print "URL: http://localhost:6060"

RPC_SERVER.serve_forever()