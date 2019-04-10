# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:55:44 2019

@author: SM Abdullah
@email: sma.csedu@gmail.com

This project aims to create some features from a provided dataset and embaded
the new features into the dataset. For the information regarding what new features
are created, please check the README file
"""

import pandas as pd
import numpy as np

# First read a dataset. This is a historial stock price dataset of Apple Inc.

df_in = pd.read_csv('dataset\AAPL.csv')

# dropping adjusted_close column, as we do not need it
df_in.drop(columns=['Adj Close'], inplace=True, axis=1)

# create a new dataframe with the existing data and a new column
column_name = list(df_in.columns)
column_name.append('Typical Price')
df_out = pd.DataFrame(data=df_in, columns=column_name)

# calculate the typical price as the mean of high, low and close price
df_out['Typical Price'] = (df_out.loc[:,'High']+df_out.loc[:,'Low']+df_out.loc[:,'Close'])/3.0

# calculating the money flow, include it in the dataframe

X = df_out.loc[:,'Typical Price'].values;
v = df_out.loc[:,'Volume'].values
money_flow = np.zeros(len(df_out))
money_flow[1:] = X[1:]*v[1:] - X[:-1]*v[:-1]
df_out['Money Flow'] = money_flow

# drop rows where money flow is equal to zero
df_out.drop(df_out[df_out['Money Flow'] == 0].index, inplace=True)

# reset index to zero
df_out.reset_index(inplace=True)

# put data on the positive and negative money flow
df_out['Positive Money Flow'] = df_out.loc[df_out['Money Flow'] > 0, 'Money Flow']
df_out['Negative Money Flow'] = abs(df_out.loc[df_out['Money Flow'] < 0, 'Money Flow'])

# drop money flow column
df_out.drop(columns='Money Flow', axis=1, inplace=True)

# cumulative sum over a sliding window of 10 days
n = 10

# create a csv file to save the dataframe
output_file = 'AAPL_' + str(n) + '.csv'

#df_out['Positive Money Flow'].fillna(0, inplace=True)
df_out['Positive Money Flow Sum'] = df_out['Positive Money Flow'].rolling(n).sum()

#df_out['Negative Money Flow'].fillna(0, inplace=True)
df_out['Negative Money Flow Sum'] = df_out['Negative Money Flow'].rolling(n).sum()

money_ratio = df_out.loc[:,'Positive Money Flow Sum'].values / df_out.loc[:,'Negative Money Flow Sum'].values

money_index = (100 * money_ratio)/ (1 + money_ratio)

# add money index as a column

df_out['Money Index'] = money_index

#df_out.fillna('', inplace=True)

df_out.to_csv(output_file)

