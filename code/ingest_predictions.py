import owlready2 as ow
import pandas as pd
import numpy as np
import csv
import datetime

## TODO: instance identifiers come in without enough specification
## should not have to hard-code instance id names

def get_local_ontology_from_file(ontology_file):
    """ return ontology class from a local OWL file """
    return ow.get_ontology("file://" + ontology_file).load()


def get_ontology_base_iri(ontology):
    """ return sring with ontology base iri """
    # TODO: this should not be hard-coded
    return "http://purl.obolibrary.org/obo/"


def save_ontology(ontology):
    """ save ontology to prespecified dir (no return) """
    today = str(datetime.date.today())
    new_onto_filename = "../ontology/instances" + today + ".owl"
    ontology.save(file = new_onto_filename, format = "rdfxml")
    print('Ontology saved to: ', new_onto_filename)


def get_class_from_ontolgy(ontology, string):
    """ return ontology class from string """
    return ontology.search_one(iri=string)


def add_instance_ids(df):
    """ return new pd.DataFrame with sequential record ID in new column """
    df['instance_id'] =  np.arange(len(df))
    return df


def get_predictions(prediction_path):
    """ return a df of instance data from csv """
    df = pd.read_csv(prediction_path)
    df = add_instance_ids(df)
    return df


def clean_instance_id(string):
    """ clean a string so that it can be used as an instance id """
    return str(string).title().strip().replace(" ", "")


def instantiate_informed_consent_form(ontology, df):
    """ create new instances of informed consent form based on predictions """
    # NOTE: need unique so we don't instantiate duplicates
    for file_id in df['fileID'].unique():
        file_id = 'fileID' + clean_instance_id(file_id)
        informed_consent_form =  get_class_from_ontolgy(ontology,
                    "http://purl.obolibrary.org/obo/ICO_0000001")(file_id)
    return ontology


def instantiate_permission_directive(ontology, df):
    """ create new instances of permission directive based on predictions """
    for idx, row in df.iterrows():
        permission_id = 'permisison' + clean_instance_id(row['instance_id'])
        permission_directive =  get_class_from_ontolgy(ontology,
                    "http://purl.obolibrary.org/obo/ICO_0000244")(permission_id)

        # add annotations to the instance
        permission_directive.text_value = [row['text']]
        permission_directive.probability = [row['px_permission']]
        permission_directive.fileID = [row['fileID']]
    return ontology


def declare_permission_form_relation(ontology, df):
    """ declare 'has_part' relation between fileID and permisison,
    return new_ontology"""
    for idx, row in df.iterrows():
        form_instance_id = get_ontology_base_iri(ontology) + 'fileID' + clean_instance_id(row['fileID'])
        form_instance = get_class_from_ontolgy(ontology, form_instance_id)
        permission_instance_id = get_ontology_base_iri(ontology) + 'permisison' + clean_instance_id(row['instance_id'])
        permission_instance = get_class_from_ontolgy(ontology, permission_instance_id)
        form_instance.has_part = [permission_instance]
    return ontology


def individual_print_test(ontology):
    """ print out individuals to stdout """
    for ind in ontology.individuals():
        print(ind.probability, ind.fileID, ind.text_value)


if __name__ == "__main__":
    prediction_path = '../data/predictions_2019-05-06.csv'
    ontology_path = '../ontology/ico.owl'

    ontology = get_local_ontology_from_file(ontology_path)
    df = get_predictions(prediction_path)

    new_ontology = instantiate_informed_consent_form(ontology, df)
    new_ontology = instantiate_permission_directive(new_ontology, df)
    new_ontology = declare_permission_form_relation(new_ontology, df)

    individual_print_test(new_ontology)
    save_ontology(new_ontology)
