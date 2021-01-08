import os
import json
import gzip
import numpy as np
import pandas as pd

#preprocessing
import string 
import nltk
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from nltk.corpus import stopwords  #stopwords
from nltk import word_tokenize,sent_tokenize # tokenizing
from nltk.stem import PorterStemmer,LancasterStemmer  # using the Porter Stemmer and Lancaster Stemmer and others
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer  # lammatizer from WordNet
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


stemmer_porter=PorterStemmer()
s_words = set(stopwords.words('english'))
punc = set(string.punctuation)

def is_only_alpha(text):
    return " ".join([word for word in text.split() if word.isalpha()])
def stemmers(llst):
    return [stemmer_porter.stem(words) for words in llst]

### load the review data

data = []
def data_clean(review_gz):
    with gzip.open(review_gz) as f:
        for l in f:
            data.append(json.loads(l.strip()))
    # first row of the list
    print(data[0])
    # convert list into pandas dataframe
    df = pd.DataFrame.from_dict(data)
    # Drop the rows I don't use in this model
    df_reviews = df.drop(['reviewTime','unixReviewTime','image','style'], axis=1) 
    #df_reviews = df[df['vote'].fillna('0')] # the fill na does not work yet. but I want it to be 0 for no votes
    df_reviews['helpful_votes'] = df_reviews['vote'] 
    df_reviews['rating'] = df_reviews['overall']
    df_reviews['reviewTitle'] = df_reviews['summary']
    df_reviews = df_reviews.drop(['overall','summary','vote'],axis=1)
    df_reviews = df_reviews.drop_duplicates(subset={"reviewerID","reviewerName","reviewText","reviewTitle"})
    #del df_reviews[['reviewTime','unixReviewTime','image','style','overall','summary','vote']]
    print('Done with loading review datadata')
    return df_reviews

def lifestyle_filter(df_meta, df_reviews):
    m = df_reviews['asin'].isin(df_meta['asin'])
    df_reviews = df_reviews[m]
    print('Done with masking the reviews to the avalable products')
    return df_review


def all_text_processing(df):
    df["all_text"] = df["reviewText"] + ' ' + df["reviewTitle"]
    df_start_reviews.dropna(subset=['all_text'], inplace=True)
    df_start_reviews['all_text'] = df_start_reviews['all_text'].str.split()
    df_start_reviews['clean_text1']= df_start_reviews['all_text'].apply(lambda words:" ".join([word for word in words if word not in s_words]))
    df_start_reviews['cleanText2'] = df_start_reviews['clean_text1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
    df_start_reviews['cleanText3'] = df_start_reviews['cleanText2'].apply(is_only_alpha)
    df_start_reviews['cleanText4'] = df_start_reviews['cleanText3'].apply(word_tokenize)
    df_start_reviews['cleanText5'] = df_start_reviews['cleanText4'].apply(lambda words: [word.lower() for word in words])
    df_start_reviews['cleanText6'] = df_start_reviews['cleanText5'].apply(stemmers)
    df_start_reviews['reviewProcessed'] = df_start_reviews['cleanText6'].apply(lambda words: " ".join(words))
    df_start_reviews = df_start_reviews.drop(['clean_text1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6'],axis=1)
    #del df[['cleanText1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6']]
    print('Done with processing review data')
    return df_processed_reviews



# how to save a csv
#imdb.to_json('imdb_processed.json')






