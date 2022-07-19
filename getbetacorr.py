import numpy as np
import pandas as pd
#used to grab the stock prices, with yahoo
import pandas_datareader as web
from datetime import datetime
#to visualize the results
import matplotlib.pyplot as plt
import seaborn
 
#select start date for correlation window as well as list of tickers
start = datetime(2015, 1, 1)
companies = list(open('/Users/arnavp4/Desktop/Capstone Project/companies'))

symbols_list = []

for company in companies:
    symbols_list.append(company.strip())

#array to store prices
symbols=[]
count = 0
#pull price using iex for each symbol in list defined above
for ticker in symbols_list: 
    r = web.DataReader(ticker, 'yahoo', start)
    # add a symbol column
    r['Symbol'] = ticker 
    symbols.append(r)
    count = count + 1
    print(ticker + " " + str(count))

# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df_pivot = df.pivot_table(index='Date', columns='Symbol', values='Close', aggfunc='sum')



corr_df = df_pivot.corr(method='pearson')
corr_df.head().reset_index()
print(corr_df)

corr_df.to_csv('/Users/arnavp4/Desktop/Capstone Project/betacorr.csv')