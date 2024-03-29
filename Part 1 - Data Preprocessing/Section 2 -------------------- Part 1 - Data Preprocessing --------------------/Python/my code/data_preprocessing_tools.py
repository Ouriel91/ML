# -*- coding: utf-8 -*-
"""Copy of data_preprocessing_tools.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jnty1fi5lYZeu9zUs6bv7diU6522z-9y

# Data Preprocessing Tools

## Importing the libraries
"""

import numpy as np # uses work with arrays (models gets array as input)
import matplotlib.pyplot as plt # uses for for charts and graphs
import pandas as pd # uses to import data sets, create matrix of featurs and dependent variable vector

"""## Importing the dataset"""

dataset = pd.read_csv('Data.csv')
# features - the colums that use for prediction of the dependent variable (not featurable column)
# these feature columns is also independent column
# here in that example - country + age + salary is feature columns that prdedict purchased column
# it means that purduct will predict if it
# purchased or not depends on country + age + salary is feature columns that feature the product
# here x is matrix of features, columns: country, age, salary, and y is dependent variable

# iloc - locate indexes, here we take indexes from dataset that we want to extract
# first parameter in iloc is rows, we take all rows - : (take everything in range)
# second parameter in iloc is columns, we take all columns till last one, the range is :-1, means
# all columns except last one
# in y we don't take range but we take the last column so it's -1 only
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# validate
print('x is: ',X)
print('y is: ',y)

"""## Taking care of missing data"""

# in dataset we have some missing data like cell without a data
# we can solve it by two ways
# 1. ignore/delete this row with missing data (usefull for large dataset - ignore/delete this row has small effect)
# 2. replace missing data in avarage of all cells in this column

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean') #all missing values will replace in average(mean)
imputer.fit(X[:, 1:3]) # first column is non numeric so let's skip it, the imputer on column 1 and 2 (3 is the edge)
X[:, 1:3]= imputer.transform(X[:, 1:3])

print(X)

"""## Encoding categorical data

### Encoding the Independent Variable
"""

# country column have string values and ml can't work with that
# we can give to France - 0, Spain - 1 and so on, but, the ml can think that
# there is some numerical order and it might cause on the prediction
# so the solution is one hot encoding, so it means turn this column into
# muliple columns as number of all column values kinds
# in our case one column turn into 3 columns (France, Spain, Germany)
# one hot encoding create binary vectors
# France turn into 100, Spain into 010, Germany - 001
# that's prevent numerical order
# in column purchase - we turn yes and no to 0 and 1

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

ct = ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[0])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

print(X)

"""### Encoding the Dependent Variable"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y) # the dependent variable (will fill in 0,1)

print(y)

"""## Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split

# we create 2 sets - one for training set and one for test set
# total - 4 sets, matrix of features and dependent variable for each 2 sets
# X_train - matrix of features for train
# X_test - matrix of features for test
# y_train - dependent variable for training set
# y_test - dependent variable for test set
# all of this is neede for ml model
# 80% observation for training set and 20% for test set
# the split setting (rows chooshing) will be randomaly, so make sure we have
# the same random factors we put random_state into 1 so we get the same split
# for two sets (without shuffle)
# see here for more details:
# https://medium.com/mlearning-ai/what-the-heck-is-random-state-24a7a8389f3d

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=1)

print('X_train: \n', X_train)
print('X_test: \n', X_test)
print('y_train: \n', y_train)
print('y_test: \n', y_test)

"""## Feature Scaling"""

# process that made for prevent some features dominating by other features
# in such way that dominate featurs not even considered by ml models
# not all ml models need feature scaling
# 2 ways for scaling: standardisation and normalizaion
# standardisation:
# (x is any value in column (feature))
# x_stand = x - mean(x)
#          -----------------------
#           standard deviation(x)
# all values will be between -3 and 3 [-3,3]
# normalizaion:
# (x is any value in column)
# x_norm = x - min(x)
#          ---------------
#          max(x) - min(x)
# all values will be between 0 and 1 [0,1]
# normalization recommended for values with noraml distribiution in most of our featurs
# standardisation is for all (or almost) cases
# we have two matrix of features - X_train and X_test so we do standardisation
# for two matrixes (reminder, spliting dataset and then feature scaling)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

# we don't need to stardardisation into dummy variables (like country feature,
# as we did before France get 100 binary value and so on)
# the reason is because the values already made for 0 and 1 which are in
# standardisation range of [-3,3]
# so we standard only age and salary features (4th and 5th column)
# fit_transform is standardisation formula
# see here why we use in X_train the fit method and in X_test the transform method
# https://towardsdatascience.com/what-and-why-behind-fit-transform-vs-transform-in-scikit-learn-78f915cf96fe
X_train[:, 3:] = sc.fit_transform(X_train[:, 3:])
X_test[:, 3:] = sc.transform(X_test[:, 3:])

print('X_train: \n', X_train)
print('X_test: \n', X_test)