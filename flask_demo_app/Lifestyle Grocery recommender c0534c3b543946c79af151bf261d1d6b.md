# Lifestyle Grocery recommender

# Start With Why?

Now with the current restrictions placed on travel and stores being closed, many people are not going to shop in physical grocery stores anymore and using delivery apps. This means that I can't browse through the store aisles anymore in order to find new and exciting foods anymore. Since the pandemic hit many more people are switching to doing all their grocery shopping online and this means an increased reliance on recommender systems to find new grocery items. I didn't think there was a good way to find similar products to ones you had but that fit your new lifestyle.

So I set out to build a new way to find your alternative favorite food that fits your lifestyle. A recommender with a website that allows visitors to input a paragraph describing the food they wished they had in their current lifestyle choice.

# Data Processing

To build a recommender like this you need a lot of product data and if possible user reviews of people describing that product. Luckily, we all know of a website that has that information. Amazon! 

I downloaded the data from [http://deepyeti.ucsd.edu/jianmo/amazon/](http://deepyeti.ucsd.edu/jianmo/amazon/). They have been scraping amazon since 1995 for research purposes. The data consists of two different files one for the metadata and the other for the reviews. 

There are 5,074,160 reviews of 287,209 products under the Amazon grocery and gourmet food category. 

Review data set columns before clean up:

reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
asin - ID of the product, e.g. 0000013714
reviewerName - name of the reviewer
vote - helpful votes of the review
style - a dictionary of the product metadata, e.g., "Format" is "Hardcover"
reviewText - text of the review
overall - rating of the product
summary - summary of the review
unixReviewTime - time of the review (unix time)
reviewTime - time of the review (raw)
image - images that users post after they have received the product

Metadata data set columns before clean up:

asin - ID of the product, e.g. 0000031852
title - name of the product
feature - bullet-point format features of the product
description - description of the product
price - price in US dollars (at time of crawl)
image - url of the product image
related - related products (also bought, also viewed, bought together, buy after viewing)
salesRank - sales rank information
brand - brand name
categories - list of categories the product belongs to
tech1 - the first technical detail table of the product
tech2 - the second technical detail table of the product
similar - similar product tab

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled.png)

After doing some initial cleaning of the data frame I ended up with two separate DataFrames one containing metadata and the other the reviews. I will join them only when needed to save from having one massive data set. 

End results in review data set columns are:

reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
asin - ID of the product, e.g. 0000013714
reviewerName - name of the reviewer
helpful_vote- helpful votes of the review
reviewText - text of the review
rating- rating of the product
review_summary - summary of the review

After dropping duplicates I ended up with unique 4,678,158 ratings. 

And for the metadata table the resulting columns are: 

asin - ID of the product, e.g. 0000031852
name - name of the product
features - bullet-point format features of the product
description - description of the product
price - price in US dollars (at time of crawl)
brand - brand name
categories - list of categories the product belongs to
main_catagory - larger classifier of Amazon most common two are 'Amazon home'  or "grocery"

# EDA

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%201.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%201.png)

count in millions

It would be nice if these reviews were more normally distributed but for the use in this recommender I could deal with this no problem. 

# Filtering the data

I am building a lifestyle grocery list recommender and that requires going through each item and seeing if they are part of the lifestyle group. In order to match each the most accuracy, I will run through the text processing part on the Metadata now in order to filter for lifestyles. 

To filter only for the foods that fit the most common modern lifestyles. I will have to play around with the main_category and the categories columns to find the right filter for my recommender. First off in the main category of Amazon home, there is 8953, but in the not amazon home there are 278098, and 25206 that are not amazon home or grocery. All of the items that are not grocery are scarce and also not grocery foods so I will drop those. 

Then I will filter for the products that include these words:

- lifestyles = ['vegetarian?','paleo?','keto?', 'vegan?','lowsugar?',"low sugar",'gluten free', "gluten",'low gluten',"pescaterian",'low fat','fat free','free fat',"organic?", "gmo",'sugar?' ,'subsitutes','indian', "Kosher", "halal", 'Ovo lacto','lacto?']

This can only do so well, as many vegetarian foods are not labeled that way. But It can do very well, now other things like free fat or organic are always labeled and should be easy to get. 

One thing I made sure to join the titles and the descriptions to make sure to catch, any indicator that mentions one of those labels. 

- The resulting DataFrame had 96,775 or almost 100,000 unique items in it.

To make sure I don't train on any reviews of products I thew out I made sure to also remove the reviews of those products. 

# Text Processing

Now I will do some natural language processing on my filtered tables. 

Before I do this I am going to work with only a random sample of 151,254 reviews due to the constraints of my computer ram. Once I am done building and testing my model I will move the pipeline and data onto an AWS Instance and work on it.

- I decided to put together the review title and review text before I do any work on it because they both have information I think is useful to vectorize.

I started using TF_IDF (which stands for Term Frequency - Inverse Term Frequency) but my data was not as clean as I had wanted so I decided to go slow and clean up the data step by step. 

1. First I wrote a custom function to get rid of any numbers in my words. I figure this is from people messing up and writing a number next to a word while typing fast. like "5while" the person miss-typed a space. 
2. Then I had to get rid of the punctuation and tokenize the words. 

Lastly I had to remove the stems from the words for example 

1. abandon/abandonment
2. absorbency/absorbent
3. marketing/markets
4. volume/volumes

So an example of where I was at this point with the 100,000 reviews is:

- 'i', 'make', 'claims', 'sports', 'nutrition', 'or', 'nutrition', 'matter', 'expertise', 'i', 'll', 'call', 'snack', 'leave', 'place', 'exercise', 'program', 'personal', 'doctor', 'nutritionist', 'coach', 'guru', 'however', 'i', 'say', 'much', 'better', 'average', 'tasting', 'sports', 'bar', 'snack', 'name', 'preference', 'free', 'cardboad', 'ish', 'stale', 'texture', 'barely', 'identifiable', 'aftertastes', 'common', 'similar', 'products', 'while', 'noone', 'compare', 'real', 'apple', 'crisp', 'convenient', 'food', 'go', 'recognizable', 'tastes', 'oats', 'this', 'flavor', 'texture', 'predominates', 'apple', 'cinnamon', 'due', 'large', 'part', 'i', 'suspect', 'fact', 'actually', 'contains', 'ingredients', 'there', 'also', 'raisins', 'cane', 'sugars', 'including', 'fructose', 'fruit', 'juices', 'giving', 'sweet', 'cloying', 'as', 'say', 'wineries', 'taste', 'this', 'company', 'known', 'quality', 'ingredients

- Once I had this data clean I ran the TF-IDF again and was amazed by how much better it did.

### What does the TF_IDF vectorizer mean for this model?

- This means that words show up a lot in our reviews, I will divide it by a large number of reviews since it doesn’t mean a lot if it's in most of the reviews. On the other hand, if a word pops up very infrequently in these reviews it’s probably much more important.

# Completing pipeline

Now I had to move my code into a pipeline that would work for the final flask app. 

This includes:

- Getting my pipeline into concise python files I can call from my app.
- Running my Text pipeline once and saving that to a .json so I don't have to re-use computing power for the most intensive part of the app.
- Running the TF-IDF once and saving it since I want to be able to recommend to users in real-time and training the model takes a couple of minutes.
- Allow a user to input text and have it run through the pipeline and be served recommendations

# Content-Based Recommender:

Once I was done with the pipeline, I was a couple of steps away from making my first prediction. One of the steps I had to do before is to make the pipeline for the incoming cosine similarity. This was fairly simple because I could convert the incoming text into the same format, a row in a Dataframe, and then run it through the pipeline. 

In order to get accurate recommendations, it is very recommended for you to run it through an identical pipeline. Once I got that ready and vectorized, I could finally get a prediction going. 

For my first prediction, all I wanted back from the recommender was the first 10 recommendations based on a user's imported product a user wished they had. 

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%202.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%202.png)

- It looked somthing like this. It returned a two lists as a tuple of the url and the item number.

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%203.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%203.png)

These results are really exciting the model caught the gluten-free feature and the predictions are almost all ones I think someone who is buying this item would like. 

After trying a couple more examples I learned some very interesting things about my model. My model picks up features and food names very well. But, if you talk about a product you wish you had without mentioning related products or plenty of features.

# Flask app

Flask is a great way to deploy websites to show your model to the world. Flask gives your model wings. I really wanted this model to be deployed. 

- "If a model is created in a jupyter notebook, was it ever created?"

I used flask in conjunction with a bootstrap template to code my website from scratch. 

I started with a couple of headers and a background picture.

How it started:

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%204.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%204.png)

Once I finished getting the buttons for each recommender system, I have something that looks like this.

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%205.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%205.png)

This is what it looked like in the end:

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%206.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%206.png)

An this is what the recommendation would look like. I would have the input the user typed. The 10 Recommendations in a table with the number the name of the item and a clickable line to amazon so that you can buy the item. 

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%207.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%207.png)

# Next Steps:

- How I would expand this model: n-grams - which would improve vocabulary
- Build an alternative food recommender - user inputs a food they like "pop tarts" and they chose their lifestyle from a checklist and get recommendations.

# Thanks!

![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%208.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%208.png)

“The biggest mistake people make in life is not trying to make a living at doing what they most enjoy.” Malcolm Forbes

## How to get jupyter notebook working on aws for capstone3

1. Amazon aws.com
2. Launch instance - deep learning ubuntu18
3. First start the g4dn instance 2xlarge or whatever size you need
4. Then in the security group, you should have port 22 open to your ip or everywhere and then custom TCP on port 8888 also your ip or everywhere

    ![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%209.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%209.png)

5. Then start the aws instance in your local machine terminal going to the connect tab in aws 

    ```bash
    ssh -i "tutorialexample.pem" ec2-user@ec2-54-144-47-199.compute-1.amazonaws.com
    ```

6. Then select the source environment

    ```bash
    source tensorflow_latest_37
    ```

7. Then run

    ```bash
    jupyter notebook --no-browser or jupyter lab --no-browser
    ```

8. Ok, now on your local machine start a terminal and connect your local port to your ec2 notebook

    ```bash
    ssh -NfL 9999:localhost:8888 -i "tutorialexample.pem" ec2-user@ec2-54-144-47-199.compute-1.amazonaws.com
    ```

9. You should get no errors after that and then you can go to your browser and copy from the aws instance terminal the last URL but change your port from 8888 to 9999

    ![Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%2010.png](Lifestyle%20Grocery%20recommender%20c0534c3b543946c79af151bf261d1d6b/Untitled%2010.png)

10.  Fin :) did you change the port to 9999? Also when you start your ipynb on the browser remember to select tensorflow_latest_37 again if you get the option

Bonus tip: Try not to use git LFS instead use SCP. To save time always send .zip files instead of tones of individual files which will bizarrely take a much longer time. 

How to scp files usually .zip files to your AWS instance from your local terminal:

scp -i ~/.ssh/mykey.pem dataFile.zip ubuntu@ec2-6-2568-121-268.compute-1.amazonaws.com:~/

How to scp things back to your own local machine from AWS. HINT: Run this from your local terminal

scp -i ~/.ssh/mykey.pem [ec2-user@ipadress.zone.compute.amazonaws.com](mailto:ec2-user@ipadress.zone.compute.amazonaws.com):~/home/path/file ~/Desktop/target

Bonus: tmux always on terminal 

```bash
tmux attach

```