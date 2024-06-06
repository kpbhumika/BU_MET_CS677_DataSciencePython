# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
this scripts reads your ticker file (e.g. MSFT.csv) and
constructs a list of lines
"""
import os
import pandas as pd


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
            df.loc[i, 'True Label'] = '-'
    return df

df_KR = add_true_label(df_KR)
df_SPY = add_true_label(df_SPY)

# Split the KR data into training and testing sets based on the years
training_stock_df_KR = df_KR[df_KR['Date'] < '2019-01-01'].copy() #Training data
testing_stock_df_KR = df_KR[df_KR['Date'] >= '2019-01-01'].copy() #Testing data

# Split the SPY data into training and testing sets based on the years
training_stock_df_SPY = df_SPY[df_SPY['Date'] < '2017-01-01'].copy() #Training data
testing_stock_df_SPY = df_SPY[df_SPY['Date'] >= '2017-01-01'].copy() #Testing data


# Calculate the probability that the next day is an "up" day
def up_probability(df):
    up = 0
    down = 0
    # Loop through each row in the DataFrame to count "up" and "down" days
    for i in range(len(df)):
        if (df.loc[i, 'True Label'] == '+'):
            up += 1
        else:
            down += 1
    probability = round((up/(up+down)) * 100,2)
    print(f"Probability p that the next day is a ”up” day is {probability}%")
    return probability


# Probability of seeing k consecutive down days followed by an up day
def consecutive_down_up_probability(df):
    for k in range(1, 4):  # k = 1, 2, 3
        down_to_up_count = 0
        down_count = 0
        consecutive_down = 0

        for i in range(len(df)):
            if df.loc[i, 'True Label'] == '-':  # Check for "down" day
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

# Question 2: Predicting labels

def find_previous_pattern(w:int, index:int, df:pd.Series )->str:
    starting_index = int(df.index[0])
    if(index<starting_index + w):
        return
    return "".join(df.loc[index-w:index-1])


def compute_predicted_labels(training_df:pd.DataFrame, testing_df:pd.DataFrame, w):

    predict_labels_count_map = {} # "--":{"+count":0,"-count":0}
    for index in  training_df.index:
        current_label = training_df['True Label'][index]
        pattern = find_previous_pattern(w,index,training_df['True Label'])
        if pattern is None:
            continue
        if(pattern not in predict_labels_count_map):
            predict_labels_count_map[pattern]={"+count":0,"-count":0}

        pattern_count = predict_labels_count_map[pattern]
        if(current_label == '+'):
            pattern_count["+count"] += 1
        else:
            pattern_count["-count"] += 1

    # Assign predicted labels for testing data

    column_name = f'Predicted Label: {w}'
    testing_df[column_name] = ''  # Initialize the column
    for index in testing_df.index:
        pattern_value = find_previous_pattern(w,index,testing_df['True Label'])
        if(pattern_value not in predict_labels_count_map):
            testing_df.loc[index,column_name] = '+' #default probability
            continue
        if(predict_labels_count_map[pattern_value]["+count"] >= predict_labels_count_map[pattern_value]["-count"]):
            testing_df.loc[index,column_name] = '+'
        else:
            testing_df.loc[index,column_name] = '-'
    return testing_df

# Compute the accuracy

def  compute_accuracy_by_sign(df,column_name, sign):
    total_samples = (df['True Label'] == sign).sum()
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    correct_predictions = ((df['True Label'] == sign) & (df['True Label'] == df[column_name])).sum()
    print(f"total_samples for {sign}:" ,total_samples)
    print(f"correct predictions for {sign}: ",correct_predictions)
    print(f"wrong predictions for {sign}:",(total_samples-correct_predictions))
    accuracy = correct_predictions / total_samples * 100
    return accuracy

# Compute ensemble labels
def majority_vote(df: pd.DataFrame):
    predicted_columns = ['Predicted Label: 2', 'Predicted Label: 3', 'Predicted Label: 4']
    df['Ensemble Label'] = ''
    for index, row in df.iterrows():
        plus_count = sum(row[col] == '+' for col in predicted_columns)
        minus_count = sum(row[col] == '-' for col in predicted_columns)
        if plus_count > minus_count:
            df.at[index, 'Ensemble Label'] = '+'
        else:
            df.at[index, 'Ensemble Label'] = '-'
    return df

def  total_accuracy(df, column_name):
    total_samples = len(df)
    if column_name not in df.columns:
        raise ValueError(f"Column {column_name}' not found in DataFrame")
    correct_predictions =  (df['True Label'] == df[column_name]).sum()
    print("correct predictions",correct_predictions)
    print("wrong predictions",total_samples-correct_predictions)
    print("total_samples", total_samples)
    accuracy = correct_predictions / total_samples * 100
    return accuracy

print("KR stock:")
up_probability(training_stock_df_KR)
consecutive_down_up_probability(training_stock_df_KR)
consecutive_up_up_probability(training_stock_df_KR)

print ("\n")
print("SPY stock:")
up_probability(training_stock_df_SPY)
consecutive_down_up_probability(training_stock_df_SPY)
consecutive_up_up_probability(training_stock_df_SPY)


W_values = [2, 3, 4]


max_accuracy_KR = {'max_accuracy': -1, 'w': None}
max_accuracy_SPY = {'max_accuracy': -1, 'w': None}

for w in W_values:
    print(f"\nPredicting labels for KR with W={w}:")
    testing_stock_df_KR = compute_predicted_labels(training_stock_df_KR, testing_stock_df_KR, w )
    print(testing_stock_df_KR)
    column_name= f'Predicted Label: {w}'
    total_accuracy_KR = total_accuracy(testing_stock_df_KR,column_name)
    print("total_accuracy_KR",total_accuracy_KR)
    accuracy_KR_up = compute_accuracy_by_sign(testing_stock_df_KR,column_name,'+')
    print(f"Accuracy for W={w} +: {accuracy_KR_up:.2f}%")
    accuracy_KR_down = compute_accuracy_by_sign(testing_stock_df_KR,column_name,'-')
    print(f"Accuracy for W={w} -: {accuracy_KR_down:.2f}%")

    if total_accuracy_KR > max_accuracy_KR['max_accuracy']:
        max_accuracy_KR['max_accuracy'] = total_accuracy_KR
        max_accuracy_KR['w'] = w

    print(f"\nPredicting labels for SPY with W={w}:")
    testing_stock_df_SPY = compute_predicted_labels(training_stock_df_SPY, testing_stock_df_SPY, w)
    print(testing_stock_df_SPY)
    total_accuracy_SPY = total_accuracy(testing_stock_df_SPY,column_name)
    print("total_accuracy_SPY",total_accuracy_SPY)
    accuracy_SPY_up = compute_accuracy_by_sign(testing_stock_df_SPY,column_name, '+')
    print(f"Accuracy for W={w} +: {accuracy_SPY_up:.2f}%")
    accuracy_SPY_down = compute_accuracy_by_sign(testing_stock_df_SPY,column_name, '-')
    print(f"Accuracy for W={w} -: {accuracy_SPY_down:.2f}%")
    if total_accuracy_SPY > max_accuracy_SPY['max_accuracy']:
        max_accuracy_SPY['max_accuracy'] = total_accuracy_SPY
        max_accuracy_SPY['w'] = w

print(f"Highest accuracy for stock KR is {round(max_accuracy_KR['max_accuracy'],2)}% for W={max_accuracy_KR['w']}")
print(f"Highest accuracy for stock SPY is {round(max_accuracy_SPY['max_accuracy'],2)}% for W={max_accuracy_SPY['w']}")

# Compute ensemble labels for KR stock for years 4 and 5
print(majority_vote(testing_stock_df_KR))
total_accuracy_KR = total_accuracy(testing_stock_df_KR,'Ensemble Label')
print("ensemble_total_accuracy",total_accuracy_KR)
accuracy_KR_up = compute_accuracy_by_sign(testing_stock_df_KR,'Ensemble Label', '+')
print(f"Accuracy for ensemble KR +: {accuracy_KR_up:.2f}%")
accuracy_KR_down = compute_accuracy_by_sign(testing_stock_df_KR,'Ensemble Label', '-')
print(f"Accuracy for ensemble KR  -: {accuracy_KR_down:.2f}%")

print(majority_vote(testing_stock_df_SPY))
total_accuracy_SPY = total_accuracy(testing_stock_df_SPY,'Ensemble Label')
print("ensemble_total_accuracy",total_accuracy_SPY)
accuracy_SPY_up = compute_accuracy_by_sign(testing_stock_df_SPY,'Ensemble Label', '+')
print(f"Accuracy for ensemble SPY +: {accuracy_SPY_up:.2f}%")
accuracy_SPY_down = compute_accuracy_by_sign(testing_stock_df_SPY,'Ensemble Label', '-')
print(f"Accuracy for ensemble SPY -: {accuracy_SPY_down:.2f}%")


csv_filename_testing = 'testing.csv'
testing_stock_df_SPY.to_csv(csv_filename_testing, index=False)

csv_filename_training = 'training.csv'
training_stock_df_SPY.to_csv(csv_filename_training, index=False)













