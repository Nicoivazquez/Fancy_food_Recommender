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

    # total length of list, this number equals total number of products
    print(len(data))

    # first row of the list
    print(data[0])

    # convert list into pandas dataframe

    df = pd.DataFrame.from_dict(data)

    print(len(df))

    df_reviews = df.drop(['reviewTime','unixReviewTime'], axis=1) # took out ,'image','style' for small 5 
    #df_reviews = df[df['vote'].fillna('0')] # the fill na does not work yet. but I want it to be 0 for no votes
    df_reviews['helpful_votes'] = df_reviews['helpful'] # change to 'vote' for small 5
    df_reviews['rating'] = df_reviews['overall']
    df_reviews['reviewTitle'] = df_reviews['summary']
    df_reviews = df_reviews.drop(['overall','summary','helpful'],axis=1)
    df_reviews = df_reviews.drop_duplicates(subset={"reviewerID","reviewerName","reviewText","reviewTitle"})
    return df_reviews

#df["all_text"] = df["reviewText"] + df["reviewTitle"]
#
"""
stemmer_porter=PorterStemmer()
from nltk.stem.snowball import SnowballStemmer
import string  
snowball_stem = SnowballStemmer(language='english')
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

"""