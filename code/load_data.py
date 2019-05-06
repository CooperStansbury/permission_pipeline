"""
Standardize data load.
"""

import os
import json
import pandas as pd


def getJSONData(annotation_file):
    """ returns a dataframe with file IDs, sentences,
    and annotation text from a JSON DataTurk output """

    new_rows = []

    with open(annotation_file) as f:
        line_count = 0 # for debugging
        for line in f: # need to load each line as a separate json object

            line_count += 1
            dat_dict = json.loads(line)
            # print(line_count)

            content = dat_dict['content'].split("]],")[1]
            fileID = dat_dict['content'].split("]],")[0].replace("[[fileID:", "")

            # all missing annotations coded as 'NON_permission_statement'
            try:
                annotation = dat_dict['annotation']['labels'][0]
            except:
                annotation = 'NON_permission_statement'

            row = {
                'annotation':annotation,
                'fileID': fileID,
                'text':content
            }

            new_rows.append(row)

    df = pd.DataFrame(new_rows)

    return df
