"""
Code before it was removed from Keras

[1]“Remove batchwise metrics ·
keras-team/keras@a56b1a5,” GitHub. [Online].
Available: https://github.com/keras-team/keras/commit/a56b1a55182acf061b1eb2e2c86b48193a0e88f7.
[Accessed: 05-Apr-2019].
"""
from tensorflow.metrics import auc as tf_auc
from tensorflow import local_variables_initializer
import keras.backend as K


def keras_precision(y_true, y_pred):
    """Precision metric.
    Only computes a batch-wise average of precision.
    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def keras_recall(y_true, y_pred):
    """Recall metric.
    Only computes a batch-wise average of recall.
    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def keras_auc(y_true, y_pred):
    """ Area under ROC """
    auc = tf_auc(y_true, y_pred)[1]
    K.get_session().run(local_variables_initializer())
    return auc


def keras_true_postives(y_true, y_pred):
    """ returns count of true positives """
    return K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
