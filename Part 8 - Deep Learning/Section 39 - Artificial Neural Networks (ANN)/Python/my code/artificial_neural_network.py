# -*- coding: utf-8 -*-
"""Copy of artificial_neural_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Yt6SqMpKWFbmWMfGsUZV8HYcf3uHM4Y6

# Artificial Neural Network

### Importing the libraries
"""

import pandas as pd
import numpy as np
import tensorflow as tf

tf.__version__

"""## Part 1 - Data Preprocessing

### Importing the dataset
"""

dataset = pd.read_csv('Churn_Modelling.csv')

#RowNumber - it's data row number and irrelevant for data prediction
#CustomerId - it's just identifier for customer and irrelevant for prediction
#Surname - the customer name is irrelvant for prediction
#so we will start from index 3 that is the diffrence between dataset and matrix of features
start_point = 3
X = dataset.iloc[:, start_point:-1].values
y = dataset.iloc[:, -1].values

#print(dataset.isnull().sum())
#print('X:\n',X)
#print('y:\n',y)

"""### Encoding categorical data

Label Encoding the "Gender" column
"""

#since we have in data two columns with lexical data and not numeric data
#so we need to encode this data
#Gender data has 2 values - male and female so we could just encode it to labeled encoding
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
gender_index = dataset.columns.get_loc('Gender') - start_point # we deleted 3 columns from X matrix of features
print(gender_index)
X[:,gender_index] = le.fit_transform(X[:,gender_index])
print(X)

"""One Hot Encoding the "Geography" column"""

#Geography data has more than 2 values
#so we need to encode it in One Hot Encoding method
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
geography_index = dataset.columns.get_loc('Geography') - start_point # we deleted 3 columns from X matrix of features
#print(geography_index)
ct = ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[geography_index])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
print(X)

"""### Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""### Feature Scaling"""

#we need to scale some columns that can be ignored
#in the prediction because values is out of range
#of dependent variable [0-1], so we scale all of the rest
#also in X_train and X_test
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#print('X train:\n',X_train)
#print('X test:\n',X_test)

"""## Part 2 - Building the ANN

### Initializing the ANN
"""

ann = tf.keras.Sequential()

"""### Adding the input layer and the first hidden layer"""

#great link and an important link for choosing the number of hidden layers and neurons number
#see the first and third answers
#https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw

#All matrix of feature will be the input(see Step 3)
#The Dense layer is the hidden layer next to the input layer.
#The input layer isn't a 'real' keras layer, it's just a place to store a tensor that says the input tensor.
#So the number of nodes of the input layer is determined by that in the input dataset.
#There is no rule of thumb how many neurons we should enter to layer
#6 is number that taken from expertise experience (see link above),
#but we can change it if we want
#by link above - number of neurons in that layer is the mean of the neurons in the input and output layers
#we use in rectifier activation function (named relu)
ann.add(tf.keras.layers.Dense(units = 6,activation='relu'))

"""### Adding the second hidden layer"""

#do the same thing in another layer
#maybe it not be needed because most of problems not require more than
#one layer (see in link above)
ann.add(tf.keras.layers.Dense(units = 6,activation='relu'))

"""### Adding the output layer"""

#the output should be only 1 neuoron, because the model is regression
#(classification have more than 1 output)
#the activation function will be sigmoid
#because we don't only need to get prediction if customer leave/not the bank
#but we also want to get the probability that customer leave the bank
ann.add(tf.keras.layers.Dense(units = 1,activation='sigmoid'))

"""## Part 3 - Training the ANN

### Compiling the ANN
"""

#adam optimizer performs stochastic gradient descent
#mean: update weights in iterations
#in order to reduce the loss error between predictions and real results
#loss function is to compute the diffrence between predictions and real results
#in binary classification that predict binary prediction(our case)
#we should use in binary_crossentropy (in non-binary classification is: crossentropy
#and activation function will be softmax instead of sigmoid)
#in metrics we could enter a list of metrics like ['accuracy','f1','precision'] etc
ann.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

"""### Training the ANN on the Training set"""

#batch size learning is more efficient and more performant in ANN
#(mean: compute the loss between predictions and real results in serval compares
#we do it in batch)
#the default value of batch size is 32
#the epochs is number trains of ANN to improve the accuracy
ann.fit(X_train, y_train, batch_size=32, epochs=100)

"""## Part 4 - Making the predictions and evaluating the model

### Predicting the result of a single observation

**Homework**

Use our ANN model to predict if the customer with the following informations will leave the bank:

Geography: France

Credit Score: 600

Gender: Male

Age: 40 years old

Tenure: 3 years

Balance: \$ 60000

Number of Products: 2

Does this customer have a credit card? Yes

Is this customer an Active Member: Yes

Estimated Salary: \$ 50000

So, should we say goodbye to that customer?
"""

single_observation = [[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]]
probability_observation = sc.transform(single_observation)
prediction = ann.predict(probability_observation)
print("Probability of customer leave the bank: " + "{:.2f}".format(prediction[0][0]*100) + "%")
print("The customer should {} bank".format('leave the' if prediction[0][0] > 0.5 else 'stay in the' ))

#also can be:
#print(ann.predict(sc.transform(ct.transform([[600,"France", le.transform(["Male"]).item() ,40,3,60000,2,1,1,50000]]

"""**Solution**

Therefore, our ANN model predicts that this customer stays in the bank!

**Important note 1:** Notice that the values of the features were all input in a double pair of square brackets. That's because the "predict" method always expects a 2D array as the format of its inputs. And putting our values into a double pair of square brackets makes the input exactly a 2D array.

**Important note 2:** Notice also that the "France" country was not input as a string in the last column but as "1, 0, 0" in the first three columns. That's because of course the predict method expects the one-hot-encoded values of the state, and as we see in the first row of the matrix of features X, "France" was encoded as "1, 0, 0". And be careful to include these values in the first three columns, because the dummy variables are always created in the first columns.

### Predicting the Test set results
"""

y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)
#print(y_pred)
y_pred_reshape = y_pred.reshape(len(y_pred),1)
y_test_reshape = y_test.reshape(len(y_test),1)
print(np.concatenate((y_pred_reshape,y_test_reshape),1))

"""### Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
print('confusion matrix:\n',confusion_matrix(y_test, y_pred))
print("accuracy_score: " + "{:.2f}".format(accuracy_score(y_test, y_pred)*100) + "%")