#!/usr/bin/env python3

"""
simple tool to run a sparql query against a local OWL file
"""

import rdflib
import pandas as pd
import argparse
import os
from tabulate import tabulate


def print_result_summary(df):
    """ print summary info to CLI """
    print(df.describe())


def run_query(owl_file, query):
    """ extract results from owl file return dataframe """
    new_rows = []
    with open(query) as q_input:
        q_data=q_input.read()
        g = rdflib.Graph()
        g = g.parse(owl_file)
        qresults = g.query(q_data)
        # iterate through query results store
        for row in qresults:
            row_dict = row.asdict()
            new_rows.append(row.asdict())
    df = pd.DataFrame(new_rows)
    print_result_summary(df)
    return(df)


def print_sample_results(df, n=10):
    """ print results to console """
    sample = df.sample(n)
    print(tabulate(sample, headers='keys', tablefmt='psql'))


def get_examples_by_permission(df, n=10):
    """ print example instances to CLI """
    sample = df.sample(n)
    for idx, row in sample.iterrows():
        print("#---------------------------------------#")
        for col in sample.columns:
            print(col, ":", row[col])
        print('\n')


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='Extract terms from local .OWL owl_file')
    parser.add_argument("--owl_file", help="owl file to query")
    parser.add_argument("--query", help="sparql query to use")
    parser.add_argument("--print", action='store_true', \
            help="if present: print output to console")
    args = parser.parse_args()

    ## handle files from args
    try:
        source_owl_file = os.path.abspath(args.owl_file)
        query_owl_file = os.path.abspath(args.query)
    except FileNotFoundError as e:
        print("Error in input arguments file paths: ", e)

    results_df = run_query(source_owl_file, query_owl_file)

    if args.print:
        # print_sample_results(results_df)
        get_examples_by_permission(results_df)
