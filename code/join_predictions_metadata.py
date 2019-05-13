#
# # non-local imports
# import pandas as pd
# import os
# import numpy as np
#
# # local imports
# from ingest_predictions import get_predictions
#
#
# def get_metadata(filepath):
#     """ retrieve metadata, return pd.DataFrame """
#     df = pd.read_csv(filepath)
#     return df
#
#
# def handle_ids(meta_df):
#     """ handle different fileID formats """
#     for id in meta_df['file_id']:
#         print(id)
#
#
#
# if __name__ == "__main__":
#     prediction_filepath = '../data/predictions_2019-05-06.csv'
#     metadata_filepath = '../data/full_metadata2019-05-02.csv'
#
#     pred_df = get_predictions(prediction_filepath)
#     meta_df = get_metadata(metadata_filepath)
#
#     for id in pred_df['fileID']:
#         print(id)
#
#
#     # handle_ids(meta_df)
#
#     # print(meta_df.head())
