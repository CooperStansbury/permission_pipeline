import pandas as pd
import re
import spacy
from keras.preprocessing import text, sequence
from sklearn.preprocessing import MultiLabelBinarizer
import string


# load once, call many
mlb = MultiLabelBinarizer()
nlp_larg = spacy.load('en_core_web_lg')


def getSentenceVectors(row):
    """ get spaCy vectors for each sent """

    sent = row['textDOC']

    return (sent.vector)


def getNounChunks(row):
    """ get spaCy noun_chunks for each sent """

    chunks = []

    sent = row['textDOC']
    for chnk in list(sent.noun_chunks):
        chunks.append(chnk.text)

    return chunks


def convertNounChunkstoOneHot(df):
    """ return a dataframe with noun_chunks as one-hot encoded
    columns """

    one_hot_chunks = pd.DataFrame(mlb.fit_transform(df.pop('noun_chunks')),
                              columns=mlb.classes_,
                              index=df.index)
    return pd.concat([df, one_hot_chunks], axis=1)


def convertVectoOneHot(df):
    """ return a dataframe with word embedding vectors
    as one-hot encoded columns """

    vec_column = ['vec_posi' + str(i) for i in range(0,300)]
    vec_df = pd.DataFrame(df['sent_vec'].values.tolist(), columns=vec_column)
    return pd.concat([df, vec_df], axis=1)


def convertSeqtoOneHot(df, maxSeen):
    """ return a dataframe with sequence """

    new_col_names = ['seq_posi' + str(i) for i in range(0,maxSeen)]
    seq_df = pd.DataFrame(df['seq_vec'].values.tolist(), columns=new_col_names)
    return pd.concat([df, seq_df], axis=1)


def convertPOSSeqtoOneHot(df, maxTokens):
    """ return a dataframe with POS sequence """

    new_col_names = ['POS_seq_posi' + str(i) for i in range(0,maxTokens)]
    pos_seq_df = pd.DataFrame(df['POS_Seq'].values.tolist(), columns=new_col_names)
    return pd.concat([df, pos_seq_df], axis=1)


def getSimpleCounts(df):
    """ return data frame with new columns of word counts """

    df['char_count'] = df['text'].apply(len)
    df['word_count'] = df['text'].apply(lambda x: len(x.split()))
    df['word_density'] = df['char_count'] / (df['word_count']+1)
    df['punctuation_count'] = df['text'].apply(lambda x: len("".join(_ for _ in x if _ in string.punctuation)))

    return df
