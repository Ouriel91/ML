# -*- coding: utf-8 -*-
"""Copy of upper_confidence_bound.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z7ZjJ8-70rtI8-NnssBb7t8dfZASe8Co

# Upper Confidence Bound (UCB)

## Importing the libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""## Importing the dataset"""

#This model is based on its own data,
#there is no need to find dependent variable,
#also we don't have matrix of features and dependent variable
#the target is to find the best solution for our need quickly and
#and test each suggestion by itself (we don't have time and money and etc for that)
# - explore (the best solution) and exploit (without iterate on each suggestion by itself)

#here we want to know which ad is the best for customer, we have serval ad
#and we want to choose the best one but not do AB test to all ads, we don't
#have all time and money for that
#we use in UCB algorithem to that (see more details in lecture)
#each user click on ad gets price and each non click of user on ad is punishment
#each row present the user and his clicks/unclicks on ad
#and each column is an ad


dataset = pd.read_csv('Ads_CTR_Optimisation.csv')
#print('nulls num:\n', dataset.isnull().sum())

#if you want to see prints of code in very small dataset subset
#just uncomment this lines and change users to number you want
#users = 50
#dataset = dataset.iloc[0:users,:]
#print(dataset)

"""## Implementing UCB"""

#this code implements the code in pdf that is found here:
#https://drive.google.com/drive/folders/1QHTYYgR6Iq6WtRHuGF6kF-Ftlf1jI4qZ

import math

users_num = len(dataset.axes[0])
ads_num = len(dataset.axes[1])
#print('total users:',users_num)
#print('total ads:',ads_num)

# ---  full round is a user ----

# Note: This does not represent a *CLICKED* ad. It is only is saying that we selected this ad to be shown to a user. 
# The user may or may not click any of these ads we've selected to show them
ads_selected = [] #full list of ads that are selected over the round (save indexes of selected ads later)

#(we the add 1 to total reward if user clicks the ad, and 0 if user don't)

#initialize array of the of times that Advertisers (not the customers!!!) selected to show ad in each round - initial value of 0
#each time we the selected ad in some number we increment this ad index in one (Array of counters)
# Note: Again, this is NOT representing clicks. It just is tracking how many times we've chosen to show each ad to a user.
times_selected_ad = [0] * ads_num

#initialize array of reward sum in ad (column) - initial value of 0 (Array of counters)
#each time that customer select this ad
# So we've selected an ad to be shown to user n, and they've clicked that ad. This list will be used for tracking how many times that happens
reward_sum = [0] * ads_num
total_reward = 0 # total reward collecte all round rewards for all customers that clicks on all ads

#print(ads_selected)
#print(times_selected_ad)
#print(reward_sum)

for i in range(0,users_num):
  ad_index = 0
  max_upper_bound = 0
  for j in range (0, ads_num):

    if(times_selected_ad[j] > 0): #the ad now already have been selected (in begining which mean the first round it will be not selected)
      average_reward = reward_sum[j] / times_selected_ad[j]
      interval_confidence = math.sqrt(3/2 * math.log(i+1) / times_selected_ad[j]) #i+1 because we start from 0 index
      upper_bound = average_reward + interval_confidence

    #the ad now not been selected (equals 0, and it's happens in first round) and the times_selected_ad[j] can't be zero,
    #because times_selected_ad it's the denominator (can't divide in 0)
    #and we need to compute the average reward (that lead to find the max upper bound)
    #hence we make sure in this else that we selected all ad for first user (first row)
    #and after ads_num rounds all the ad will be selected and we will skip else condition
    else:
      upper_bound =  1e400 #super high value like infinity

    # as loop through our ads_num, we use this max_upper_bound to track which of our 10 ads has the highest upper_bound
    if(max_upper_bound < upper_bound):
        max_upper_bound = upper_bound
        ad_index = j

  # after this for loop has cycled through our ads_num, whatever ad had the highest upper_bound will be assigned to ad_index = j
  # so if our first ad had the highest upper bound, ad = 0
  # THIS IS OUR CHOSEN AD WE'RE GOING TO SHOW TO USER n
  ads_selected.append(ad_index)
  times_selected_ad[ad_index] += 1
  reward = dataset.values[i, ad_index]
  reward_sum[ad_index] += reward
  total_reward += reward
  #print('selected ads table: ',times_selected_ad)
  #print('reward sum table:', reward_sum)
  #print("User #{}, select ad {} with reward of {}".format(i+1, ad_index+1,dataset.values[i, ad_index]))
  #print('total_reward', total_reward)
  #print('\n')

"""## Visualising the results"""

plt.hist(ads_selected)
plt.title('Histogram of ads selections')
plt.xlabel('Ads')
plt.ylabel('Number of times each ad was selected')
plt.show()