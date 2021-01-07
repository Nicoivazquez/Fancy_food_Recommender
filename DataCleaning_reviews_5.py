import os
import json
import gzip
import pandas as pd

### load the meta data for small data set

data = []
def data_clean(meta_gz):
    with gzip.open(meta_gz) as f:
        for l in f:
            data.append(json.loads(l.strip()))

    # convert list into pandas dataframe

    df = pd.DataFrame.from_dict(data)


    df_reviews = df.drop(['reviewTime','unixReviewTime'], axis=1) # took out ,'image','style' for small 5 
    #df_reviews = df[df['vote'].fillna('0')] # the fill na does not work yet. but I want it to be 0 for no votes
    df_reviews['helpful_votes'] = df_reviews['helpful'] # change to 'vote' for small 5
    df_reviews['rating'] = df_reviews['overall']
    df_reviews['reviewTitle'] = df_reviews['summary']
    df_reviews = df_reviews.drop(['overall','summary','helpful'],axis=1)
    df_reviews = df_reviews.drop_duplicates(subset={"reviewerID","reviewerName","reviewText","reviewTitle"})
    print('Done with loading meta5 data')
    return df_reviews

