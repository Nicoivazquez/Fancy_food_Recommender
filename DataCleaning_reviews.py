import os
import json
import gzip
import pandas as pd

### load the meta data

data = []
with gzip.open('../Grocery_and_Gourmet_Food.json.gz') as f:
    for l in f:
        data.append(json.loads(l.strip()))
    
# total length of list, this number equals total number of products
print(len(data))

# first row of the list
print(data[0])

# convert list into pandas dataframe

df = pd.DataFrame.from_dict(data)

print(len(df))