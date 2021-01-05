import os
import json
import gzip
import pandas as pd


### load the meta data

meta = []
with gzip.open('../meta_Grocery_and_Gourmet_Food.json.gz') as f:
    for l in f:
        meta.append(json.loads(l.strip()))
    
# total length of list, this number equals total number of products
print(len(meta))

# first row of the list
print(meta[0])

# convert list into pandas dataframe

meta_df = pd.DataFrame.from_dict(meta)

print(len(meta_df))

### remove rows with unformatted title 

meta_df = meta_df.fillna('') # or do I keep it na
#df5 = df3[~df3.title.str.contains('getTime')] # filter those unformatted rows
print(len(df5))

meta_df = meta_df.drop(['tech1','fit','also_buy', 'image','tech2', 'also_view','similar_item','date',''])
# gives you df with ['category', 'tech1', 'description', 'fit', 'title', 'also_buy', 'image',
#        'tech2', 'brand', 'feature', 'rank', 'also_view', 'main_cat',
#        'similar_item', 'date', 'price', 'asin', 'details'

# 287051 products

