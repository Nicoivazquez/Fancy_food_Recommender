import os
import json
import gzip
import pandas as pd

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

### load the meta data

data = []
def data_clean(meta_gz):
    with gzip.open(meta_gz) as f:
        for l in f:
            data.append(json.loads(l.strip()))

    # total length of list, this number equals total number of products
    print(len(data))

    # first row of the list
    print(data[0])

    # convert list into pandas dataframe

    df = pd.DataFrame.from_dict(data)

    print(len(df))

    df_reviews = df.drop(['reviewTime','unixReviewTime','image','style], axis=1) 
    #df_reviews = df[df['vote'].fillna('0')] # the fill na does not work yet. but I want it to be 0 for no votes
    df_reviews['helpful_votes'] = df_reviews['vote'] 
    df_reviews['rating'] = df_reviews['overall']
    df_reviews['reviewTitle'] = df_reviews['summary']
    df_reviews = df_reviews.drop(['overall','summary','vote'],axis=1)
    df_reviews = df_reviews.drop_duplicates(subset={"reviewerID","reviewerName","reviewText","reviewTitle"})
    return df_reviews

                          # how to save a csv
#imdb.to_csv('imdb_processed.csv', index=False)
                          
# def lifestyle():
#     def is_only_alpha(text):
#         return " ".join([word for word in text.split() if word.isalpha()])
#     def stemmers(llst):
#         return [stemmer_porter.stem(words) for words in llst]
#     df_meta_life['cleanText1']= df_meta_life['all_text'].apply(lambda words:" ".join([word for word in words.split() if word not in s_words]))
#     df_meta_life['cleanText2'] = df_meta_life['cleanText1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
#     df_meta_life['cleanText3'] = df_meta_life['cleanText2'].apply(is_only_alpha)
#     df_meta_life['cleanText4'] = df_meta_life['cleanText3'].apply(word_tokenize)
#     df_meta_life['cleanText5'] = df_meta_life['cleanText4'].apply(lambda words: [word.lower() for word in words])
#     df_meta_life['cleanText6'] = df_meta_life['cleanText5'].apply(stemmers)
#     df_meta_life['cleanText7'] = df_meta_life['cleanText6'].apply(lambda words: " ".join(words))              
                          
#     lifestyles = ['vegetarian?','paleo?','keto?', 'vegan?','lowsugar?',"low sugar",'gluten free', "gluten",'low gluten',"pescaterian",'low fat','fat free','free fat',"organic?", "gmo",'sugar?' ,'subsitutes','indian', "Kosher", "halal", 'Ovo lacto','lacto?']
#     df_meta_filtered = df_meta_life[df_meta_life['cleanText7'].str.contains('|'.join(lifestyles))]
                        
                        


                          