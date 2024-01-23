# -*- coding: utf-8 -*-
"""Copy of natural_language_processing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1APdfvrMggEOlBtsIyrE0IK-7m6icbe7w

# Natural Language Processing

## Importing the libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""## Importing the dataset"""

#simple option
#dataset = pd.read_csv('Restaurant_Reviews.tsv', sep='\t')
#print(dataset)
#print(dataset.isnull().sum())

#another option
#You can use a delimiter to separate data, quoting = 3 helps to clear quotes in datasst
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)
#print(dataset)
#print(dataset.isnull().sum())

#that is for taking small piece of dataset and see in prints what is going now
#un comment this lines for that
#reviews = 1
#dataset = dataset.iloc[0:reviews,:]
#print(dataset)

"""## Cleaning the texts"""

#similar process to data preprocessing
#text have punctuation, diffrent characters, capital letters, lowercase,
#verb are conjugated diffrently.. and we will simplify that and clean text

import re #libary that helps us to simplify the reviews
#library that allow us to ensemble stop words
#stop words - words that we don't want to include after cleaning text
#mean: words that we don't want (after cleaning) to include in reviews that
#not relevant for positive/negative review, example: "the", "a" ...
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
#apply stemming on our reviews
#means: take root of word, for example stem of word loved will be love
#the root of love is enough to positive review predict
#that will help to bag of words stage and create sparse metrix from that and minimize it
from nltk.stem.porter import PorterStemmer

corpus = [] #will contain all cleaned reviews

for i in range(0, len(dataset)):
  clean_review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])#replace everything that is not a letter in space
  #print('clean review',clean_review)
  clean_review = clean_review.lower()#all capital letters will transform into lowercase
  #print('clean review',clean_review)
  clean_review = clean_review.split()#split different elements in reviews into different words
  #print('clean review',clean_review)
  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  #print('all stop words', all_stopwords)
  all_stopwords.remove('not') #not is negative term and important to prediction
  #print('all stop words', all_stopwords)
  clean_review = [ps.stem(word) for word in clean_review if not word in set(all_stopwords)]#clean stop words (that splitted before)
  #print('clean review',clean_review)
  clean_review = ' '.join(clean_review)#join these words into one sentence that is cleaned review (space between words)
  #print('clean review',clean_review)
  corpus.append(clean_review)

arr = np.array(corpus)
newarr = arr.reshape(len(corpus), 1)
print(newarr)

#pay attention: tasty printed as tasti
#That's due to stemming. For example:
#easy and easily are both stemmed to easi so they are identified and no longer distinguished.

"""## Creating the Bag of Words model"""

from sklearn.feature_extraction.text import CountVectorizer
#we choose the most frequent words that will help us to predict positive/negative review
#to make the sparse matrix efficient (tokenization)
#we put max_features to 1500
#to get rid of words that not useful for prediction like name of person (like Steve)
cv = CountVectorizer(max_features=1500)
X = cv.fit_transform(corpus).toarray() #feature of matrix should be 2D
y = dataset.iloc[:, -1].values #dependent variable

#find how many words we have from tokenization that create vector
#print the first row provide the number (compare it if CountVectorizer() is empty (it's 1566))
print(len(X[0]))

"""## Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""## Training the Naive Bayes model on the Training set"""

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

"""## Predicting the Test set results"""

y_pred = classifier.predict(X_test)

y_pred_reshape = y_pred.reshape(len(y_pred),1)
y_test_reshape = y_test.reshape(len(y_test),1)
print(np.concatenate((y_pred_reshape,y_test_reshape),1))

"""## Making the Confusion Matrix"""

from sklearn.metrics import accuracy_score, confusion_matrix
print('confusion matrix:\n',confusion_matrix(y_test, y_pred))
print("accuracy_score: " + "{:.2f}".format(accuracy_score(y_test, y_pred)*100) + "%")