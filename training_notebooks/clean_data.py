
import re
import spacy


# load once, call many
nlp_larg = spacy.load('en_core_web_lg')

"""
The following citation is for the language library developed by spaCy authors:


[1] Models for the spaCy Natural Language Processing (NLP) library: explosion/spacy-models.
Explosion, 2019.

English multi-task CNN trained on OntoNotes, with GloVe vectors trained on Common Crawl.
Assigns word vectors, context-specific token vectors, POS tags, dependency parse and named entities. This is
what allows us to predict...
"""

### --------------------- 'APPLY' FUNCTIONS --------------------- ###

def minimalTextCleaning(row, field):
    """ perform text processing on raw data to new field """

    # force encoding
    encoded_text = row[field].encode(encoding = 'ascii',errors = 'replace')
    decoded_text = encoded_text.decode(encoding='ascii',errors='strict')
    remove_funky_chars = str(decoded_text).replace("?", " ")
    lower_case = str(remove_funky_chars).lower().strip()

    # strip redundant whitespace
    cleaned_text = re.sub(' +', ' ', lower_case)


    # strip signature lines
    cleaned_text = cleaned_text.replace("_", "")

    return cleaned_text


def getDocObjects(row, field):
    """ return spacy doc object from a text field """

    doc = nlp_larg(str(row[field]).lower())

    return doc


def getSentenceList(row, field):
    """ return list of sentences from doc object field;
    each item will be token span """

    return list(row[field].sents)


def cleanSents(row, field):
    """ perform minor text cleaning on all sents """

    text = str(row[field]).lower()
    clean_text = re.sub('[^A-Za-z0-9]+', ' ', text).strip()
    return clean_text


def convertAnnotationtoBinary(row, field):
    """ return binary (0,1), where 1 = permission_statement """

    if str(row[field]).__contains__('NON'):
        return 0
    else:
        return 1
