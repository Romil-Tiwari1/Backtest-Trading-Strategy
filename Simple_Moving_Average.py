import yfinance as yf
import numpy as np

# Define the ticker symbol
tickerSymbol = 'AAPL'

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-12-31')

import matplotlib.pyplot as plt

# Calculate the moving averages
tickerDf['Fast_SMA'] = tickerDf['Close'].rolling(window=50).mean()
tickerDf['Slow_SMA'] = tickerDf['Close'].rolling(window=200).mean()

# Create a column 'Signal' such that if Fast SMA is greater than Slow SMA then 1 else 0
tickerDf['Signal'] = 0.0  
tickerDf['Signal'] = np.where(tickerDf['Fast_SMA'] > tickerDf['Slow_SMA'], 1.0, 0.0)

# Create a column 'Position' which is the difference of 'Signal' column
tickerDf['Position'] = tickerDf['Signal'].diff()

# Initialize the portfolio with value owned   
portfolio, cash = 0, 10000  # cash is our initial amount in USD
tickerDf['Holdings'] = 0.0
tickerDf['Cash'] = cash

# The next lines are for the loop, where we will simulate the trading
for i in range(len(tickerDf)):
    # Simulating the BUY
    if tickerDf['Position'].iloc[i] == 1:  # A buy signal
        portfolio = cash / tickerDf['Close'].iloc[i]
        cash = 0
        tickerDf['Holdings'].iloc[i] = portfolio * tickerDf['Close'].iloc[i]
        tickerDf['Cash'].iloc[i] = cash
    # Simulating the SELL
    elif tickerDf['Position'].iloc[i] == -1:  # A sell signal
        cash = portfolio * tickerDf['Close'].iloc[i]
        portfolio = 0
        tickerDf['Holdings'].iloc[i] = portfolio * tickerDf['Close'].iloc[i]
        tickerDf['Cash'].iloc[i] = cash
    # If there is no signal, we just carry forward the values
    else:
        tickerDf['Holdings'].iloc[i] = portfolio * tickerDf['Close'].iloc[i]
        tickerDf['Cash'].iloc[i] = cash

# Calculating the total balance (holdings + cash)
tickerDf['Total'] = tickerDf['Holdings'] + tickerDf['Cash']


# See your data
print(tickerDf.head())

# Plot closing price, fast SMA, and slow SMA
# Visualizing the signals

plt.figure(figsize=(12,6))
plt.plot(tickerDf['Total'])
plt.title('Total Portfolio Value Over Time')
plt.xlabel('Date')
plt.ylabel('Portfolio Value in $')
plt.grid(True)
plt.show()

# See your data
print(tickerDf.head())
