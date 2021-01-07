
import DataCleaning_meta
import DataCleaning_reviews

# data visualisation and manipulation
import numpy as np
import pandas as pd
import pickle
#preprocessing
import string 
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from nltk.corpus import stopwords  #stopwords
from nltk import word_tokenize,sent_tokenize # tokenizing
from nltk.stem import PorterStemmer,LancasterStemmer  # using the Porter Stemmer and Lancaster Stemmer and others
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer  # lammatizer from WordNet
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

def is_only_alpha(text):
    return " ".join([word for word in text.split() if word.isalpha()])
def stemmers(llst):
    return [stemmer_porter.stem(words) for words in llst]

# setting up stemmer, stopwords, and punctuation.
stemmer_porter=PorterStemmer()
s_words = set(stopwords.words('english'))
punc = set(string.punctuation)
vectorizer = TfidfVectorizer(max_features=10_000, lowercase=False)
item_asin_top10 = []
top10_url = []

def text_to_vec(col):
    vec_X_train = vectorizer.fit_transform(col)
    with open('mypklvec.pkl', 'wb') as f:
        pickle.dump(vectorizer,f)
    return vec_X_train


# X is the tf-idf of the reviews 
# y is the target or the inputed review from the user
def input_to_pred(user_input, saved_model,review_df):
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
    user_x = vectorizer.transform([user_df['processed_text'][0]])
    sim_matrix = cosine_similarity(user_x,saved_model)
    sim_sorted = np.argsort(sim_matrix)[::-1] # idx of lowest value to highest value but with ::-1 its decending
    #df['processed_text'][sim_sorted[0][-1]] # looks like it works better going backwards
    #Geting the text that was most similar to the user input but not needed for flask app url is
    for i in range(10):
        item_asin_top10.append(review_df.iloc[sim_sorted[0][-i]].loc['asin']) # works filtering backwards
    for asin in item_asin_top10:
        url = "http://www.amazon.com/dp/"+asin
        top10_url.append(url)
    return top10_url




if __name__ == "__main__":
    user_input = input('what is the userText')
    # import meta data and then filter them
    df_start_meta = DataCleaning_meta.data_clean_meta("../meta_Grocery_and_Gourmet_Food.json.gz")
    # filter the lifestyle sections I want
    df_lifestyle_meta = DataCleaning_meta.lifestylefilter(df_start_meta)
    # bring in the reviews and select only the ones in the meta data
    df_start_reviews = DataCleaning_reviews.data_clean('../Grocery_and_Gourmet_Food.json.gz')
    df_processed_reviews = DataCleaning_reviews.all_text_processing(df_start_reviews)
    #load saved model in the future
    #saved_model = .pkl
    saved_model = text_to_vec(df_processed_reviews['reviewProcessed'])


    urls = input_to_pred(user_input, saved_model,df_processed_reviews)

    print(urls)