"""
Standardize data load across notebooks
"""

import os
import json
import pandas as pd

def getDIRData(directory):
    """ returns a dataframe with cleaned filenames, full paths,
    and unprocessed text from a directory of informed consent forms """

    new_rows = []

    fileID = 0

    # iterate through directory
    for subdir, dirs, files in os.walk(directory):
        for file in files:

            # assign each file an id, might be handy later
            fileID += 1
            filepath = subdir + os.sep + file

            # this is unnecessary now, but easy edge-case
            if filepath.endswith('.txt'):

                # read file contents to str
                with open(filepath, 'r') as myfile:
                    data = myfile.read().replace('\n', ' ')

                # by adding dicts to list we can speed up
                # data.frame creation
                new_rows.append(
                    {
                        'id': fileID,
                        'name':str(file),
                        'path':filepath,
                        'rawText':data
                    }
                )

    df = pd.DataFrame(new_rows)
    return df


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
