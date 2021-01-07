import os
import json
import gzip
import pandas as pd
import string
#preprocessing
import nltk
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from nltk.corpus import stopwords  #stopwords
from nltk import word_tokenize,sent_tokenize # tokenizing
from nltk.stem import PorterStemmer,LancasterStemmer  # using the Porter Stemmer and Lancaster Stemmer and others
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer  # lammatizer from WordNet

stemmer_porter=PorterStemmer()
s_words = set(stopwords.words('english'))
punc = set(string.punctuation)

def is_only_alpha(text):
    return " ".join([word for word in text.split() if word.isalpha()])
def stemmers(llst):
    return [stemmer_porter.stem(words) for words in llst]

### load the meta data

meta = []
def data_clean_meta(meta_gz):
    with gzip.open('../meta_Grocery_and_Gourmet_Food.json.gz') as f:
        for l in f:
            meta.append(json.loads(l.strip()))

    # total length of list, this number equals total number of products
    print(len(meta))

    # first row of the list
    print(meta[0])

    # convert list into pandas dataframe
    meta_df = pd.DataFrame.from_dict(meta)
    meta_df = meta_df.fillna('') 
    # drop things I don't see use for curently
    meta_df = meta_df.drop(['tech1','fit','also_buy', 'image','tech2', 'also_view','similar_item','date','details'], axis=1)
    # gives you df with ['category', 'tech1', 'description', 'fit', 'title', 'also_buy', 'image',
    #        'tech2', 'brand', 'feature', 'rank', 'also_view', 'main_cat',
    #        'similar_item', 'date', 'price', 'asin', 'details'

    # 287051 products
    # rename the confusing columns
    meta_df['name'] = meta_df['title']
    meta_df['features'] = meta_df['feature']
    meta_df['categories'] = meta_df['category']
    meta_df['main_category'] = meta_df['main_cat']
    meta_df = meta_df.drop(['main_cat','title','feature','category'], axis = 1)
    # this code removes the list of the categories and descriptions
    meta_df['description']= meta_df['description'].apply(lambda words: " ".join(words)) 
    meta_df['categories']= meta_df['categories'].apply(lambda words: " ".join(words))
    # this code joins categories and description in order to text precess all text
    meta_df['all_text'] = meta_df['description'] + ' ' + meta_df['name']
    meta_df['all_text'] = meta_df['all_text'] + ' ' + meta_df['categories']
    # filter all the home kitchen products away
    meta_df = meta_df[meta_df['main_category'] == 'Grocery']
    return meta_df

def lifestylefilter(df_meta_life):
    df_meta_life['cleanText1']= df_meta_life['all_text'].apply(lambda words:" ".join([word for word in words.split() if word not in s_words]))
    df_meta_life['cleanText2'] = df_meta_life['cleanText1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
    df_meta_life['cleanText3'] = df_meta_life['cleanText2'].apply(is_only_alpha)
    df_meta_life['cleanText4'] = df_meta_life['cleanText3'].apply(word_tokenize)
    df_meta_life['cleanText5'] = df_meta_life['cleanText4'].apply(lambda words: [word.lower() for word in words])
    df_meta_life['cleanText6'] = df_meta_life['cleanText5'].apply(stemmers)
    df_meta_life['lifestyle_processed'] = df_meta_life['cleanText6'].apply(lambda words: " ".join(words))
    df_meta_life = df_meta_life.drop(['cleanText1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6'],axis=1)
    lifestyles = ['vegetarian?','paleo?','keto?', 'vegan?','lowsugar?',"low sugar",'gluten free', "gluten?",'low gluten',"pescaterian?",'low fat','fat free','free fat',"organic?", "gmo",'sugar?' ,'subsitutes?','indian?', "Kosher?", "halal?", 'Ovo lacto','lacto?']
    df_meta_life_filtered = df_meta_life[df_meta_life['lifestyle_processed'].str.contains('|'.join(lifestyles))]

    return df_meta_life_filtered


