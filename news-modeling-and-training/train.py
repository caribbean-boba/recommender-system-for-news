import cnn_model
import numpy as np
import os
import pandas as pd
import pickle
import shutil
import tensorflow as tf

from sklearn import metrics

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = './model/'
DATA_SET_FILE = './labeled_news.csv'
VARS_FILE = './vars'
VOCAB_PROCESSOR_SAVE_FILE = './vocab_procesor_save_file'
MAX_DOCUMENT_LENGTH = 100
N_CLASSES = 8

STEPS = 200

def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        print("Delete old models...")
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # Load data
    df = pd.read_csv(DATA_SET_FILE, header=None)
    train_df = df[0:400]
    test_df = df.drop(train_df.index)

    # x is feature 'title', Y is class
    x_train = train_df[1]
    Y_train = train_df[0]
    x_test = test_df[1]
    Y_test = test_df[0]

    # Process the document with VocabularyProcessoro
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))

    n_words = len(vocab_processor.vocabulary_)
    print('Total words after VocabularyProcessor: %d' % n_words)

    with open(VARS_FILE, 'wb') as f:
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    # Initialize new Moodel!
    classifier = learn.Estimator(
        model_fn=cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # Fit
    classifier.fit(x_train, Y_train, steps=STEPS)

    # Evaluate 
    Y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]

    score = metrics.accuracy_score(Y_test, Y_predicted)
    print('Accuracy is: {0:f}'.format(score))

if __name__ == '__main__':
    tf.app.run(main=main)