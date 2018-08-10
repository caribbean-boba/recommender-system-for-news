"""
Two layer CNN in this model
"""
import tensorflow as tf

EMBEDDING_SIZE = 40
POOLING_WINDOW = 4
POOLING_STRIDE = 2


LEARNING_RATE = 0.05

N_FILTERS = 10
WINDOW_SIZE = 20
FILTER_SHAPE1 = [WINDOW_SIZE, EMBEDDING_SIZE]
FILTER_SHAPE2 = [WINDOW_SIZE, N_FILTERS]

def generate_cnn_model(num_classes, num_words):
    """Use 2 layers in the model."""
    def cnn_model(features, target):
      # Create embeddings and map

      target = tf.one_hot(target, num_classes, 1, 0)
      word_vectors = tf.contrib.layers.embed_sequence(
          features, vocab_size=num_words, embed_dim=EMBEDDING_SIZE, scope='words')
      word_vectors = tf.expand_dims(word_vectors, 3)

      # First Layer here!!!!!!!
      with tf.variable_scope('CNN_MODEL_layer1'):
        # First layer convolution filtering on sequence
        conv1 = tf.contrib.layers.convolution2d(
            word_vectors, N_FILTERS, FILTER_SHAPE1, padding='VALID')
        # First layler adding a RELU for non linearity.
        conv1 = tf.nn.relu(conv1)
        # First layler  Max pooling
        pool1 = tf.nn.max_pool(
            conv1,
            ksize=[1, POOLING_WINDOW, 1, 1],
            strides=[1, POOLING_STRIDE, 1, 1],
            padding='SAME')
        pool1 = tf.transpose(pool1, [0, 1, 3, 2])

      # Second Layer here!!!!!!!
      with tf.variable_scope('CNN_MODEL_layer2'):
        conv2 = tf.contrib.layers.convolution2d(
            pool1, N_FILTERS, FILTER_SHAPE2, padding='VALID')
        # Max across each filter to get useful features for classification.
        pool2 = tf.squeeze(tf.reduce_max(conv2, 1), squeeze_dims=[1])

      # Fully_conncted pool2 and classes
      logits = tf.contrib.layers.fully_connected(pool2, num_classes, activation_fn=None)
      loss = tf.contrib.losses.softmax_cross_entropy(logits, target)

      train_op = tf.contrib.layers.optimize_loss(
          loss,
          tf.contrib.framework.get_global_step(),
          optimizer='Adam',
          learning_rate=LEARNING_RATE)

      return ({
          'class': tf.argmax(logits, 1),
          'prob': tf.nn.softmax(logits)
      }, loss, train_op)

    return cnn_model