import pandas as pd
import numpy as np
import json
import get_permissions

from tensorflow.metrics import auc as tf_auc
from tensorflow import local_variables_initializer
import keras
import keras.backend as K
from keras.models import model_from_yaml
from keras.preprocessing import text, sequence
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Conv2D, \
        MaxPooling1D, LSTM, Flatten, BatchNormalization,Embedding,Reshape, Dropout


def get_new_column_names(maxlen):
    """ return list of new column names """
    print('Generating', str(maxlen), 'new column names...')
    return ['seq_posi' + str(i) for i in range(0,maxlen)]


def prepare_data(df, vocabulary_size, maxlen):
    """ preprocess data before predicting, return new dataFrame """

    print('Preprocessing data based on vocab size: ', str(vocabulary_size))
    print('Using maximum sequence length: ', str(maxlen))

    # tokenize according to vocab size
    tokenizer = Tokenizer(num_words= vocabulary_size)
    tokenizer.fit_on_texts(df['text'])

    # get text sequences
    sequences = tokenizer.texts_to_sequences(df['text'])
    data = pad_sequences(sequences, maxlen=maxlen)
    df['data'] = data.tolist()

    # add text seuqences to new columns
    new_col_names = get_new_column_names(maxlen)
    pos_seq_df = pd.DataFrame(df['data'].values.tolist(), columns=new_col_names)
    return pd.concat([df, pos_seq_df], axis=1)


def get_model(model_path, mapping_path):
    """ load trained keras model for predictions """
    print('Loading model from: ', str(model_path))
    print('Loading mappings from: ', str(mapping_path))

    # load YAML and create model
    yaml_file = open(mapping_path, 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    print('YAML Loaded.')
    loaded_model = model_from_yaml(loaded_model_yaml)
    # load weights into new model
    loaded_model.load_weights(model_path)
    return loaded_model


def get_class_predictions(loaded_model, df, maxlen):
    """ get predicted classes, return new pd.DataFrame with preds
    1 = permission, 0 = !permission """
    print('Making class predictions based on default cut-off = .5')
    print('1 = permission, 0 = !permission.')

    new_col_names = get_new_column_names(maxlen)
    predictions = loaded_model.predict_classes(df[new_col_names])
    df['predictions'] = predictions.tolist()
    return df


def get_probability_predictions(loaded_model, df, maxlen):
    """ get probability of predictions in new columns """
    print('Returning probabilities of predicting postive class.')
    print('1 = permission, 0 = !permission.')
    new_col_names = get_new_column_names(maxlen)
    predictions = loaded_model.predict_proba(df[new_col_names])
    df['probabilities'] = predictions.tolist()

    prob_df = pd.DataFrame(df['probabilities'].values.tolist(),
                columns=['px_not_permission', 'px_permission'])

    return pd.concat([df, prob_df], axis=1)


def get_positive_predictions(df, threshold):
    """ return pd.DataFrame with only positive predictions """
    print('Getting positive predictions for p(x) >= ', str(threshold))
    return df.loc[df['px_permission'] >= threshold]


def print_sample_of_postive_preds(df, threshold, n_samples):
    """ print a random sample of positive predictions """
    print('Getting' , str(n_samples), 'random samples for threshold',
                                        str(threshold))
    print('##### POSITIVE SAMPLES #####')
    df = df.loc[df['px_permission'] >= threshold]
    df = df.sample(n=n_samples)

    for idx, row in df.iterrows():
        print('px:',row['px_permission'],'--', row['text'])


def save_postives_to_file(df, threshold):
    """ save postive predictions to file for ingestion into ontology """

    import datetime
    today = str(datetime.date.today())
    file_name = '../data/predictions_' + today + '.csv'

    print('Saving predictions at ', str(threshold), 'to',
                str(file_name))

    import datetime
    today = str(datetime.date.today())

    df = df.loc[df['px_permission'] >= threshold]
    df['threshold_used'] = str(threshold)
    df['export_date'] = today

    df.to_csv(file_name, index=False)
    print('Saved', len(df), 'predictions to: ', file_name)


# -------------------- Fake Main -------------------- #
# relative file paths
file_path = '../data/ALL_CANDIDATES.json'
model_path = '../models/CNN_model2019-04-19.h5'
mapping_path = '../models/CNN_model2019-04-19.yaml'

# build df
df = get_permissions.getJSONData(file_path)
print('Data Loaded.')

df = prepare_data(df, 1000, 100)
print('Data Prepared.')

loaded_model = get_model(model_path,mapping_path)
print('Model Loaded.')

# df = get_class_predictions(loaded_model, df, 100)
# print('Class Predictions Made.')

df = get_probability_predictions(loaded_model, df, 100)
print('Predictions Made, p(x) saved to new column.')

# positives_df = get_positive_predictions(df, .5)
# print('Positive Predictions Extracted.')

# print_sample_of_postive_preds(df, .9, 10)

save_postives_to_file(df, .75)
