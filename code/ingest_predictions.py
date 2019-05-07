import owlready2 as ow
import pandas as pd
import numpy as np
import csv
import datetime


def getOntology(ontology_file):
    """ return ontology class from a local OWL file """
    return ow.get_ontology("file://" + ontology_file).load()


def get_class_from_ontolgy(ontology, string):
    """ return ontology class from string """
    return ontology.search_one(iri=string)


def get_predictions(prediction_path):
    """ return a df of instance data from csv """
    df = pd.read_csv(prediction_path)
    df['instance_id'] =  np.arange(len(df))
    return df


def instantiatePermissionDirective(ontology, df):
    """ create new instances of permission directive based on predictions """
    for idx, row in df.iterrows():
        permission_id = str(row['instance_id']).title().strip().replace(" ", "")
        # instantiate a new class based on value from csv file
        permission_direcive =  get_class_from_ontolgy(ontology,
                    "http://purl.obolibrary.org/obo/ICO_0000244")(permission_id)

        permission_direcive.comment = [row['text']] # add text as comment
    return ontology


def instantiateInformedConsentForm(ontology, df):
    """ create new instances of informed consent form based on predictions """
    # NOTE: need unique so we don't instantiate duplicates
    for file_id in df['fileID'].unique():
        file_id = str(file_id).title().strip().replace(" ", "")
        # instantiate a new class based on value from csv file
        informed_consent_form =  get_class_from_ontolgy(ontology,
                    "http://purl.obolibrary.org/obo/ICO_0000001")(file_id)


    return ontology

# ## ---------------------- fake main ------------------------------------ ##
prediction_path = '../data/predictions_2019-05-06.csv'
ontology_path = '../ontology/ico.owl'

ontology = getOntology(ontology_path)
df = get_predictions(prediction_path)

new_ontology = instantiatePermissionDirective(ontology, df)
new_ontology = instantiateInformedConsentForm(new_ontology, df)

# TODO: specify relation between
# TODO: get fileID name/metadata


# print individals to command line
for ind in new_ontology.individuals():
    print(ind.comment)

# save new ontology to file
today = str(datetime.date.today())
new_onto_filename = "../ontology/instances" + today + ".owl"
new_ontology.save(file = new_onto_filename, format = "rdfxml")
