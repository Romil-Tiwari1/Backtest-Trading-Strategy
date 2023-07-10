import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

tickerSymbol = 'AAPL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2023-7-10')

# Calculate 20 Day Moving Average, Std Deviation, Upper Band and Lower Band
tickerDf['20 Day MA'] = tickerDf['Close'].rolling(window=20).mean()
tickerDf['20 Day STD'] = tickerDf['Close'].rolling(window=20).std()
tickerDf['Upper Band'] = tickerDf['20 Day MA'] + (tickerDf['20 Day STD'] * 2)
tickerDf['Lower Band'] = tickerDf['20 Day MA'] - (tickerDf['20 Day STD'] * 2)

import matplotlib.pyplot as plt

# Create a new DataFrame
df = tickerDf[['Close','20 Day MA','Upper Band','Lower Band']].copy()

# Create 'Signal' column such that if Close price is lower than the Lower Band then BUY (signal = 1)
# If Close price is higher than the Upper Band then SELL (signal = -1)
df['Signal'] = 0  # initialize the column with zeros
df.loc[df['Close'] < df['Lower Band'], 'Signal'] = 1  # buy signal
df.loc[df['Close'] > df['Upper Band'], 'Signal'] = -1  # sell signal

# Create 'Position' column
df['Position'] = df['Signal'].replace(0, np.nan).fillna(method='ffill')

# Create Buy and Sell columns
df['Buy'] = np.where(df['Signal'] == 1, df['Close'], np.nan)
df['Sell'] = np.where(df['Signal'] == -1, df['Close'], np.nan)

# Plotting
plt.figure(figsize=(12,5))
plt.grid(True)
plt.plot(df['Close'], label='Close Price', color='blue', alpha=0.35)
plt.plot(df['20 Day MA'], label='Moving Average', color='red', alpha=0.35)
plt.scatter(df.index, df['Buy'], color='green', label='Buy Signal', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red', label='Sell Signal', marker='v', alpha=1)
plt.fill_between(df.index, df['Lower Band'], df['Upper Band'], alpha=0.1, color='orange')
plt.title('AAPL Bollinger Band (20,2)')
plt.xlabel('Date (Year/Month)')
plt.ylabel('Price')
plt.legend(loc='best')
plt.show()
