
import DataCleaning_meta_copy
import DataCleaning_reviews_copy

# data visualisation and manipulation
import numpy as np
import pandas as pd
import pickle
#preprocessing
import string 
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from nltk.corpus import stopwords  #stopwords
from nltk import word_tokenize,sent_tokenize # tokenizing
from nltk.stem import PorterStemmer,LancasterStemmer  # using the Porter Stemmer and Lancaster Stemmer and others
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer  # lammatizer from WordNet
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


# setting up stemmer, stopwords, and punctuation.
stemmer_porter=PorterStemmer()
s_words = set(stopwords.words('english'))
punc = set(string.punctuation)
vectorizer = TfidfVectorizer(max_features=10_000, lowercase=False)
item_asin_top10 = []
top10_url = []


def is_only_alpha(text):
    return " ".join([word for word in text.split() if word.isalpha()])
def stemmers(llst):
    return [stemmer_porter.stem(words) for words in llst]


def text_to_vec(col):
    vec_X_train = vectorizer.fit_transform(col)
    with open('mypklvec.pkl', 'wb') as f:
        pickle.dump(vectorizer,f)
    with open('mypkltrain.pkl','wb') as t:
        pickle.dump(vec_X_train,t)
    return vec_X_train


# X is the tf-idf of the reviews 
# y is the target or the inputed review from the user
def input_to_pred(user_input, vecpkl,modelpkl, review_df): #
    user_df = pd.DataFrame({'user1': [user_input]})
    user_df['cleanText1']= user_df['user1'].apply(lambda words:" ".join([word for word in words.split() if word not in s_words]))
    user_df['cleanText2'] = user_df['cleanText1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
    user_df['cleanText3'] = user_df['cleanText2'].apply(is_only_alpha)
    user_df['cleanText4'] = user_df['cleanText3'].apply(word_tokenize)
    user_df['cleanText5'] = user_df['cleanText4'].apply(lambda words: [word.lower() for word in words])
    user_df['cleanText6'] = user_df['cleanText5'].apply(stemmers)
    user_df['processed_text'] = user_df['cleanText6'].apply(lambda words: " ".join(words))
    user_df = user_df.drop(['cleanText1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6'],axis=1)
    # Now that the user input went though the text processer I run it though the same vectorizer 
    user_x = vecpkl.transform([user_df['processed_text'][0]])
    sim_matrix = cosine_similarity(user_x,modelpkl)
    sim_sorted = np.argsort(sim_matrix)[::-1] # idx of lowest value to highest value but with ::-1 its decending
    #df['processed_text'][sim_sorted[0][-1]] # looks like it works better going backwards
    #Geting the text that was most similar to the user input but not needed for flask app url is
    counter = 1
    while len(item_asin_top10) < 10:
        asin = review_df.iloc[sim_sorted[0][-counter]].loc['asin'] # works filtering backwards
        counter += 1
        if asin not in item_asin_top10:
            item_asin_top10.append(str(asin))
        else: 
            continue
    for asin in item_asin_top10:
        url = "http://www.amazon.com/dp/"+asin
        top10_url.append(url)
    return top10_url, item_asin_top10

def input_to_pred_jac(user_input, vecpkl,modelpkl, review_df):
    user_df = pd.DataFrame({'user1': [user_input]})
    user_df['cleanText1']= user_df['user1'].apply(lambda words:" ".join([word for word in words.split() if word not in s_words]))
    user_df['cleanText2'] = user_df['cleanText1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
    user_df['cleanText3'] = user_df['cleanText2'].apply(is_only_alpha)
    user_df['cleanText4'] = user_df['cleanText3'].apply(word_tokenize)
    user_df['cleanText5'] = user_df['cleanText4'].apply(lambda words: [word.lower() for word in words])
    user_df['cleanText6'] = user_df['cleanText5'].apply(stemmers)
    user_df['processed_text'] = user_df['cleanText6'].apply(lambda words: " ".join(words))
    user_df = user_df.drop(['cleanText1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6'],axis=1)
    # Now that the user input went though the text processer I run it though the same vectorizer 
    user_x = vecpkl.transform([user_df['processed_text'][0]])
    sim_matrix = jaccard_score(user_x,modelpkl)
    sim_sorted = np.argsort(sim_matrix)[::-1] # idx of lowest value to highest value but with ::-1 its decending
    #df['processed_text'][sim_sorted[0][-1]] # looks like it works better going backwards
    #Geting the text that was most similar to the user input but not needed for flask app url is
    counter = 1
    while len(item_asin_top10) < 10:
        asin = review_df.iloc[sim_sorted[0][-counter]].loc['asin'] # works filtering backwards
        counter += 1
        if asin not in item_asin_top10:
            item_asin_top10.append(str(asin))
        else: 
            continue
    for asin in item_asin_top10:
        url = "http://www.amazon.com/dp/"+asin
        top10_url.append(url)
    return top10_url, item_asin_top10
