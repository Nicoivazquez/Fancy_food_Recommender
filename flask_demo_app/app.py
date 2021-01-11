from flask import Flask, render_template, url_for, request
import numpy as np
from sklearn.datasets import load_iris
import pickle
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64
import random
import DataCleaning_meta_copy
import DataCleaning_reviews_copy
import Content_model_app
import os
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


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home(title=None):
    title="Home"
    return render_template("home.html", title=title)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/eda', methods=['POST','GET'])
def eda():
    column_options = [1, 2, 3, 4]
    return render_template("eda.html", column_options=column_options)

@app.route('/graphs', methods=['POST'])
def graphs():
    col1 = int(request.form['column1']) - 1
    col2 = int(request.form['column2']) - 1

    if col1 == col2:
        return f'Why do you want to graph column {col1+1} by itself?!'
    else:
        fig = Figure()
        ax = fig.subplots()
        ax.scatter([random.random() for i in range(100)], [random.random() for i in range(100)])
        ax.set_title('A Very Random Scatterplot')
        pngImage = BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        image = pngImageB64String
        return render_template('graphs.html', col1=col1+1, col2=col2+1, url=f'./static/images/col{col1}col{col2}.png', image=image)

@app.route('/predict',methods=['POST','GET'])
def predict():
    return render_template('predict.html')

@app.route('/results', methods=['POST','GET'])
def results():
    user_name = str(request.form['user_name'])
    user_input = str(request.form['user_input'])



        # import meta data and then filter them
    #df_start_meta = DataCleaning_meta.data_clean_meta("../meta_Grocery_and_Gourmet_Food.json.gz")
    # filter the lifestyle sections I want
    #df_lifestyle_meta = DataCleaning_meta.lifestylefilter(df_start_meta)
    #df_lifestyle_meta.to_json('df_lifestyle_meta.json')
    ########df_lifestyle_meta = pd.read_json('../df_lifestyle_meta.json')
    # bring in the reviews and process all the text for vecorizer
    # df_start_reviews = DataCleaning_reviews.data_clean('../Grocery_and_Gourmet_Food.json.gz')
    #select only the ones in the lifestyle meta data
    # df_start_reviews = DataCleaning_reviews.lifestyle_filter(df_lifestyle_meta, df_start_reviews)
    # df_processed_reviews = DataCleaning_reviews.all_text_processing(df_start_reviews)
    # df_processed_reviews.to_json('df_processed_reviews.json')
    # df_processed = pd.read_json('../df_processed_reviews_5.json')
    df_processed_reviews = pd.read_json('./ziopDf/df_processed_filltered_reviews.json')
    #saved_model = text_to_vec(df_processed_reviews['reviewProcessed'])
    #load saved model in the future




    
    urls = Content_model_app.input_to_pred(user_input, vectorizer ,model, df_processed_reviews) #
    df_urls = pd.DataFrame(list(zip(urls[0],urls[1])), columns= ['Url', 'asin'])
    # rememeber to pass the red_def from the function once you got the urls
    #df_lifestyle_meta = pd.read_json('./ziopDf/df_lifestyle_meta.json').set_index('asin')
    df_to_show_products = pd.read_json('./ziopDf/df_to_show_products.json')
    rec_df = df_urls.merge(df_to_show_products, on='asin', how='left')
    your_list = "Your List"
    print(rec_df.head())
    return render_template('results.html',name=user_name, rec_df=rec_df,user_input=user_input)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__=="__main__":

    pickle_vec =  "./ziopDf/mypklvec.pkl"
    pickle_model = "./ziopDf/mypkltrain.pkl"
    model_path =  pickle_model
    vectorizer_path = pickle_vec
    vectorizer = pickle.load(open(vectorizer_path,'rb'))
    model = pickle.load(open(model_path,'rb'))


    app.run(debug=True, host='0.0.0.0', port=8105, threaded=True)
    
