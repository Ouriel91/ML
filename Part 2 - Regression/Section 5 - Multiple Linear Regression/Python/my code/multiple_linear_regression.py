# -*- coding: utf-8 -*-
"""Copy of multiple_linear_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19glGVaogKzm5ouMok_6R-dIypZCJMiUt

# Multiple Linear Regression

## Importing the libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""## Importing the dataset"""

dataset = pd.read_csv('50_Startups.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

print("nulls: \n", dataset.isnull().sum())
#print(X)
#print(y)

"""## Encoding categorical data"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# encode state column
ct = ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[3])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

print(X)

"""## Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)

"""## Training the Multiple Linear Regression model on the Training set"""

# this LinearRegression library avoid us from get into dummy variable trap
# we don't need to remove some columns that made by OneHotEncoder
# this LinearRegression library to all the backward elimination technique

from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train, y_train)

"""## Predicting the Test set results"""

# the diffrent between simple linear regression and mulitple linear regression is
# that we have more features than simple linear regression (4 in that case vs 1)
# since we have sevral features we can't plot graph (we have featurs that need
# to shown in more than 2D graph - that's impossible)
# so we display two vectors:
# the 20% (test size - test set) of real profit from the test set
# the 20% (test size - test set) of predicted profit from the test set
# and we compare the vectors and see if the predicted profit close to real profit

y_pred = lr.predict(X_test)

# display numerical value only two decimals after point (comma)
np.set_printoptions(precision=2)

# concatenate tuple (of arrays) we want to concatenate(vectors in that case)
# it must to be in same shape like here the real & predicted profit is the same
# (test size 20%, and the same structure 1D array in that case)
# reshape shapes the array diffrently, 1 is show vertically
y_pred_reshape = y_pred.reshape(len(y_pred),1)
y_test_reshape = y_test.reshape(len(y_test),1)

# the 1 here is axis - 1 means do vertical concate
print(np.concatenate((y_pred_reshape,y_test_reshape),1))

"""### Making a single prediction (for example the profit of a startup with R&D Spend = 160000, Administration Spend = 130000, Marketing Spend = 300000 and State = 'California')"""

print(lr.predict([[1,0,0,160000,130000,300000]]))

"""Therefore, our model predicts that the profit of a Californian startup which spent 160000 in R&D, 130000 in Administration and 300000 in Marketing is $ 181566,92.

Important note 1: Notice that the values of the features were all input in a double pair of square brackets. That's because the "predict" method always expects a 2D array as the format of its inputs. And putting our values into a double pair of square brackets makes the input exactly a 2D array. Simply put:

1,0,0,160000,130000,300000→scalars

[1,0,0,160000,130000,300000]→1D array

[[1,0,0,160000,130000,300000]]→2D array

Important note 2: Notice also that the "California" state was not input as a string in the last column but as "1, 0, 0" in the first three columns. That's because of course the predict method expects the one-hot-encoded values of the state, and as we see in the second row of the matrix of features X, "California" was encoded as "1, 0, 0". And be careful to include these values in the first three columns, not the last three ones, because the dummy variables are always created in the first columns.

## Getting the final linear regression equation with the values of the coefficients
"""

print(lr.coef_)
print(lr.intercept_)

"""Therefore, the equation of our multiple linear regression model is:

$$\textrm{Profit} = 86.6 \times \textrm{Dummy State 1} - 873 \times \textrm{Dummy State 2} + 786 \times \textrm{Dummy State 3} + 0.773 \times \textrm{R&D Spend} + 0.0329 \times \textrm{Administration} + 0.0366 \times \textrm{Marketing Spend} + 42467.53$$

**Important Note:** To get these coefficients we called the "coef_" and "intercept_" attributes from our regressor object. Attributes in Python are different than methods and usually return a simple value or an array of values.
"""