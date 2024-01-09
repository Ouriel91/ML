# -*- coding: utf-8 -*-
"""Copy of logistic_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16P9z7e5RL-fzDTQpehrksP18a86GYxoo

# Logistic Regression

## Importing the libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""## Importing the dataset"""

dataset = pd.read_csv('Social_Network_Ads.csv')
X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values

#print('X:\n', X)
#print('y:\n', y)
#print('nulls num:\n', dataset.isnull().sum())

"""## Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
# test size of 25% means that test set contains 100 customers - round number (not madatory)
# the proportions between train and test set should be: 80-20 / 75-25
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# print('X_train:\n', X_train)
# print('X_test:\n', X_test)
# print('y_train:\n', y_train)
# print('y_test:\n', y_test)

"""## Feature Scaling"""

# feature scaling to Estimated salary column (fit to purchased column)
# they should be in same range, so we do scaling of standardization
# see here why we use in X_train the fit method and in X_test the transform method
# https://towardsdatascience.com/what-and-why-behind-fit-transform-vs-transform-in-scikit-learn-78f915cf96fe
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# print('X_train:\n', X_train)
# print('X_test:\n', X_test)

"""## Training the Logistic Regression model on the Training set"""

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train,y_train)

"""## Predicting a new result"""

# predict single result as an example, customer that in 30 years old and earns 87000
# we need to scale it again because we scaled whole X_train and so on but
# not for one row, so the predict method can predict with same scalers as above (X_train etc)
# but for now he need to scaled again for this single prediction
is_purchased= classifier.predict(sc.transform([[30,87000]]))
print('car purchased? ')
print('No' if is_purchased == 0 else 'Yes')

"""## Predicting the Test set results"""

y_pred = classifier.predict(X_test)
# print(y_pred)
y_pred_reshape = y_pred.reshape(len(y_pred),1)
y_test_reshape = y_test.reshape(len(y_test),1)
print(np.concatenate((y_pred_reshape,y_test_reshape),1))

"""## Making the Confusion Matrix"""

# confusion matrix show the number of correct predictions
# briefly, at last code cell it looks like we have lot of
# correct predictions and model need to be very accurate
from sklearn.metrics import confusion_matrix, accuracy_score
print('confusion matrix:\n',confusion_matrix(y_test, y_pred))
print("accuracy_score: " + "{:.2f}".format(accuracy_score(y_test, y_pred)*100) + "%")

# matrix results:
# [
#   [65  3]
#   [ 8 24]
# ]
# predictions of:
# corect prediction - top left result 00 - people that not purchase the car and the prediction was they won't purchase the car
# incorect prediction - bottom left result 01 - people that not purchase the car and the prediction was they will purchase the car
# incorect prediction - top right result 10 - people that purchase the car and the prediction was they won't purchase the car
# corect prediction - bottom right result 11 - people that purchase the car and the prediction was they purchase the car

# accuary: whole test set = 100 rows
# correct predictions = 89 (65+24)
# incorrect predictions = 11 (3+8)
# total accuary = 89%

"""## Visualising the Training set results"""

# we will create a 2D plot - with the curve line (in that case it will be staright)
# (as should be in classification - see in lectures)
# the region are the classes that who that not purchased the car - 0
# and who that purchased the car - 1
# the line seperate between two regions

from matplotlib.colors import ListedColormap
# set two variables at once, transform the X_train from feature scaling
X_set, y_set = sc.inverse_transform(X_train), y_train

# numpy.meshgrid - Return a list of coordinate matrices from coordinate vectors.
# good explain - https://www.sharpsightlabs.com/blog/numpy-meshgrid/
# official docs - https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html

# take all values from age column, take the min from all values (18) and subtract 10
# (my estimation is the marks of each 10 years in the plot) - that start range
# print(X_set[:, 0].min() - 10)
# take all values from age column, take the min from all values (50) and add 10 - that stop range
# print(X_set[:, 0].max() - 10)
# each step in grid will be 0.25. like 10, 10.25, 10.5 ... - make dense grid (lot predictions to compute)
# that's create the side of ages in grid (X axis)
# do the same in Y axis that will be for estimated salary with 1000 marks in plot
# that a preperation for plot the contours.

X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 0.25),
                     np.arange(start = X_set[:, 1].min() - 1000, stop = X_set[:, 1].max() + 1000, step = 0.25))
# print('X1:\n',X1)
# print('X2:\n',X2)

# Plot filled contours.
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contourf.html

# numpy ravel:
# Return a contiguous flattened array.
# A 1-D array, containing the elements of the input, is returned. A copy is made only if needed.
# https://numpy.org/doc/stable/reference/generated/numpy.ravel.html
# T:
# View of the transposed array.
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html
# array shape:
# Tuple of array dimensions.
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html

plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('salmon', 'dodgerblue')))

# Get or set the x/y limits of the current axes.
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xlim.html
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

# enumrate
# https://www.geeksforgeeks.org/enumerate-in-python/

# numpy unique
# Find the unique elements of an array.
# https://numpy.org/doc/stable/reference/generated/numpy.unique.html

# draw points on graph (0 - no, 1 - yes)
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('salmon', 'dodgerblue'))(i), label = j)

plt.title('Logistic Regression (Training set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

# red/blue actual point - actually results of not/yes purchase (someone purchase/not)
# red/blue prdediction region(class) - prediction of not/yes purchase (as above but model prediction)
# the prediction boundary (line in middle) is where the classifier seperates between two classes
# the one reason that prediction curve (the boundary) is straight line and not curve line it because Logistic Regression is linear model

"""## Visualising the Test set results"""

from matplotlib.colors import ListedColormap
X_set, y_set = sc.inverse_transform(X_test), y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 0.25),
                     np.arange(start = X_set[:, 1].min() - 1000, stop = X_set[:, 1].max() + 1000, step = 0.25))
plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('salmon', 'dodgerblue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('salmon', 'dodgerblue'))(i), label = j)
plt.title('Logistic Regression (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()