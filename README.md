# New features creation of an existing dataset

This project talks about how we can create some features based on what we have in a dataset. I will demonastrate through a stock dataset and show how to create multiple new features and add them in the existing dataset.

## What you will learn from this project
This project mainly convers data processing using Pandas. By checking this project, one may learn the following topics
1. How to create a new column in a dataframe
2. How to manipulate a column from other columns
3. How to create columns based on certain conditions
4. How sliding window works on Pandas
5. How to save the dataframe as a CSV file.

The scenario for creating new features are presented below

## Money Flow Index
The money flow index (MFI) is a momentum indicator that measures the inflow and outflow of money into and out of a security over a specific period of time. It is computed as below, and can assume values between 0 to 100.   

Money Flow Index = 100 * Money Ration/(1+Money Ratio)   
Money Ratio = Positive Money Flow Sum / Negative Money Flow Sum   
Money Flow = Typical Price * Volume   
Typical Price = (High Price + Low Price + Close Price) / 3     

The concepts of Positive and Negative Money Flow are defined as follows: on any given day, the Money Flow is denoted positive/negative if the Typical Price is higher/lower than the previous day's Typical Price. If the typical price is unchanged that that day's data are discarded. The Positive Money Flow Sum is the sum of all the Positive Money Flow over a sliding window of n days. The Negative Money Flow Sum is similarly defined. 
