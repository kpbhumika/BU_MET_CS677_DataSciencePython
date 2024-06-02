# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
this scripts reads your ticker file (e.g. MSFT.csv) and
constructs a list of lines
"""
import os
import pandas as pd



ticker = 'KR'
input_dir = os.getcwd()
ticker_file_KR = os.path.join(input_dir, 'KR' + '.csv')
ticker_file_SPY = os.path.join(input_dir, 'SPY' + '.csv')

df_KR = pd.read_csv(ticker_file_KR)
df_SPY = pd.read_csv(ticker_file_SPY)


# Question 1:
# Add 'True Label' column
def add_true_label(df):
    for i in range(len(df)):
        if df.loc[i, 'Return'] >= 0:
            df.loc[i, 'True Label'] = '+'
        else:
            df.loc[i, 'True Label'] = '−'
    return df

df_KR = add_true_label(df_KR)
df_SPY = add_true_label(df_SPY)

# Split the KR data into training and testing sets based on the years
training_stock_df_KR = df_KR[df_KR['Date'] < '2019-01-01'].copy() #Training data
testing_stock_df_KR = df_KR[df_KR['Date'] >= '2019-01-01'].copy() #Testing data

# Split the SPY data into training and testing sets based on the years
training_stock_df_SPY = df_SPY[df_SPY['Date'] < '2017-01-01'].copy() #Training data
testing_stock_df_SPY = df_SPY[df_SPY['Date'] >= '2017-01-01'].copy() #Testing data


# Question 2:
def up_probability(df):
    up = 0
    down = 0
    # Loop through each row in the DataFrame to count "up" and "down" days
    for i in range(len(df)):
        if (df.loc[i, 'True Label'] == '+'):
            up += 1
        else:
            down += 1
    # Calculate the probability that the next day is an "up" day
    probability = round((up/(up+down)) * 100,2)
    print(f"Probability p that the next day is a ”up” day is {probability}%")
    return probability

# Question 3:
# Probability of seeing k consecutive down days followed by an up day
def consecutive_down_up_probability(df):
    for k in range(1, 4):  # k = 1, 2, 3
        down_to_up_count = 0
        down_count = 0
        consecutive_down = 0

        for i in range(len(df)):
            if df.loc[i, 'True Label'] == '−':  # Check for "down" day
                consecutive_down += 1
            else:
                if consecutive_down == k:  # Found k consecutive "down" days
                    down_count += 1
                    # Check if the next day is "up"
                    if (i + 1 < len(df) and df.loc[i + 1, 'True Label']) == '+':
                        down_to_up_count += 1
                consecutive_down = 0

        if down_count > 0:
            probability = round((down_to_up_count / down_count) * 100, 2)
        else:
            probability = 0
        print(f"Probability of seeing {k} consecutive down days followed by an up day: {probability}%")
    return probability


# Question 4:
# Probability of seeing k consecutive up days followed by another up day
def consecutive_up_up_probability(df):
    for k in range(1, 4):  # k = 1, 2, 3
        up_to_up_count = 0
        up_count = 0
        consecutive_up = 0

        for i in range(len(df)):
            if df.loc[i, 'True Label'] == '+':  # Check for "up" day
                consecutive_up += 1
            else:
                if consecutive_up == k:  # Found k consecutive "up" days
                    up_count += 1
                    # Check if the next day is also "up"
                    if (i + 1 < len(df) and df.loc[i + 1, 'True Label']) == '+':
                        up_to_up_count += 1
                consecutive_up = 0

        if up_count > 0:
            probability = round((up_to_up_count / up_count) * 100, 2)
        else:
            probability = 0

        print(f"Probability of seeing {k} consecutive up days followed by another up day: {probability}%")
    return probability

print("KR stock:")
up_probability(training_stock_df_KR)
consecutive_down_up_probability(training_stock_df_KR)
consecutive_up_up_probability(training_stock_df_KR)

print ("\n")
print("SPY stock:")
up_probability(training_stock_df_SPY)
consecutive_down_up_probability(training_stock_df_SPY)
consecutive_up_up_probability(training_stock_df_SPY)










