
import DataCleaning_meta
import DataCleaning_reviews

# data visualisation and manipulation
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
df['cleanText1']= df['all_text'].apply(lambda words:" ".join([word for word in words.split() if word not in s_words]))
df['cleanText2'] = df['cleanText1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
df['cleanText3'] = df['cleanText2'].apply(is_only_alpha)
df['cleanText4'] = df['cleanText3'].apply(word_tokenize)
df['cleanText5'] = df['cleanText4'].apply(lambda words: [word.lower() for word in words])
df['cleanText6'] = df['cleanText5'].apply(stemmers)
df['cleanText7'] = df['cleanText6'].apply(lambda words: " ".join(words))
df = df.drop(['cleanText1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6'],axis=1)

vectorizer = TfidfVectorizer(max_features=10_000, lowercase=False)
X = vectorizer.fit_transform(df['cleanText7'])

# X is the tf-idf of the reviews 
# y is the target or the inputed review from the user
y = vectorizer.transform(["Broth It was great!"])

from sklearn.metrics.pairwise import cosine_similarity
sim_matrix = cosine_similarity(y,X)
sim_sorted= np.argsort(sim_matrix)[::-1] # idx of lowest value to highest value but with ::-1 its decending
sim_sorted
df['cleanText7'][sim_sorted[0][-1]] # looks like it works better going backwards




# X is the tf-idf of the reviews 
# y is the target or the inputed review from the user
user_input = "I want a marinara sauce that tastes similar to how my mom makes it with fresh tomatoes, garlic, basil, and olive oil."
user_df = pd.DataFrame({'user1': [user_input]})
def is_only_alpha(text):
    return " ".join([word for word in text.split() if word.isalpha()])
def stemmers(llst):
    return [stemmer_porter.stem(words) for words in llst]
user_df['cleanText1']= user_df['user1'].apply(lambda words:" ".join([word for word in words.split() if word not in s_words]))
user_df['cleanText2'] = user_df['cleanText1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
user_df['cleanText3'] = user_df['cleanText2'].apply(is_only_alpha)
user_df['cleanText4'] = user_df['cleanText3'].apply(word_tokenize)
user_df['cleanText5'] = user_df['cleanText4'].apply(lambda words: [word.lower() for word in words])
user_df['cleanText6'] = user_df['cleanText5'].apply(stemmers)
user_df['cleanText7'] = user_df['cleanText6'].apply(lambda words: " ".join(words))
#user_df = df.drop(['cleanText1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6'],axis=1)
y = vectorizer.transform([user_df['cleanText7'][0]])

#Geting the text that was most similar to the user input but not needed for flask app
#df['cleanText7'][sim_sorted[0][-2]]

item_asin_top10 = []
for i in range(10):
    item_asin_top10.append(df.iloc[sim_sorted[0][-i]].loc['asin'])
top10_url = []
for asin in item_asin_top10:
    url = "http://www.amazon.com/dp/"+asin
    top10_url.append(url)
top10_url


