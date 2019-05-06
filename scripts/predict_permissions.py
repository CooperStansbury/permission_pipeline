import pandas as pd
import numpy as np
import json
import load_data


full_data ='../data/ALL_CANDIDATES.json'
df = load_data.getJSONData(full_data)
print(df.head())
