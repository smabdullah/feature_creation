# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:55:44 2019

@author: SM
"""

import pandas as pd
import numpy as np

df_input = pd.read_csv('AAPL.csv')

# dropping adjusted_close column
df_input.drop(columns=['Date', 'Adj Close'], inplace=True, axis=1)

# create a new dataframe
column_name = ['Open', 'High', 'Low', 'Close', 'Volume', 'Typical Price']
df_output = pd.DataFrame(data=df_input, columns=column_name)

# calculate the typical price as the mean of high, low and close price

df_output['Typical Price'] = (df_output.loc[:,'High']+df_output.loc[:,'Low']+df_output.loc[:,'Close'])/3.0

# calculating the money flow

X = df_output.loc[:,'Typical Price'].values;
v = df_output.loc[:,'Volume'].values
money_flow = np.zeros(1007)
money_flow[1:] = X[1:]*v[1:] - X[:-1]*v[:-1]
df_output['Money Flow'] = money_flow

# drop rows where money flow is equal to zero
df_output.drop(df_output[df_output['Money Flow'] == 0].index, inplace=True)

# put data on the positive and negative money flow
df_output['Positive Money Flow'] = df_output.loc[df_output['Money Flow'] > 0, 'Money Flow']
df_output['Negative Money Flow'] = abs(df_output.loc[df_output['Money Flow'] < 0, 'Money Flow'])

# drop money flow column
df_output.drop(columns='Money Flow', axis=1, inplace=True)

# reset index to zero
df_output.reset_index(inplace=True)

# cumulative sum over a sliding window of 10 days
n = 10
df_output['Positive Money Flow'].fillna(0, inplace=True)
df_output['Positive Money Flow Sum'] = df_output['Positive Money Flow'].rolling(n).sum()

df_output['Negative Money Flow'].fillna(0, inplace=True)
df_output['Negative Money Flow Sum'] = df_output['Negative Money Flow'].rolling(n).sum()

money_ratio = df_output.loc[:,'Positive Money Flow Sum'].values / df_output.loc[:,'Negative Money Flow Sum'].values

money_index = (100 * money_ratio)/ (1 + money_ratio)

# add money index as a column

df_output['Money Index'] = money_index

df_output.fillna('', inplace=True)

df_output.to_csv('output.csv')

