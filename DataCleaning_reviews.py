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

df_reviews = df.drop(['reviewTime','unixReviewTime','image','style'], axis=1)
#df_reviews = df[df['vote'].fillna('0')] # the fill na does not work yet. but I want it to be 0 for no votes
df_reviews['helpful_votes'] = df_reviews['vote']
df_reviews['rating'] = df_reviews['overall']
df_reviews['reviewTitle'] = df_reviews['summary']
df_reviews = df_reviews.drop(['overall','summary','vote'],axis=1)
