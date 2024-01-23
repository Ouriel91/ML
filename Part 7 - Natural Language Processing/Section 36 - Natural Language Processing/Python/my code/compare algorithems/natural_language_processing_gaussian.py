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
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

"""## Cleaning the texts"""

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

corpus = [] 

for i in range(0, len(dataset)):
  clean_review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
  clean_review = clean_review.lower()
  clean_review = clean_review.split()
  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  clean_review = [ps.stem(word) for word in clean_review if not word in set(all_stopwords)]
  clean_review = ' '.join(clean_review)
  corpus.append(clean_review)

arr = np.array(corpus)
newarr = arr.reshape(len(corpus), 1)
print(newarr)

"""## Creating the Bag of Words model"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1500)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, -1].values 

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