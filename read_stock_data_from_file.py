# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
this scripts reads your ticker file (e.g. MSFT.csv) and
constructs a list of lines
"""
import os
import pandas as pd

ticker='KR'
input_dir = os.getcwd()
ticker_file = os.path.join(input_dir, ticker + '.csv')

try:
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(ticker_file)

    # Add the True Label column
    for i in range(len(df)):
        if df.loc[i, 'Return'] >= 0:
            df.loc[i, 'True Label'] = '+'
        else:
            df.loc[i, 'True Label'] = '−'

    # Save the updated DataFrame to a new CSV file
    output_file = os.path.join(input_dir, ticker + '_trueLabeled.csv')
    df.to_csv(output_file, index=False)
    print('Saved labeled data to file:', output_file)


except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)












