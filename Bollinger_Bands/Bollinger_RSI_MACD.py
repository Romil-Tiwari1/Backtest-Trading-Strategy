import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Download historical data for required stocks
ticker = "AAPL"
tickerDf = yf.download(ticker, start='2010-1-1', end='2023-12-31')

# Bollinger Bands
tickerDf['MA20'] = tickerDf['Close'].rolling(window=20).mean()
tickerDf['20dSTD'] = tickerDf['Close'].rolling(window=20).std()
tickerDf['Upper'] = tickerDf['MA20'] + (tickerDf['20dSTD'] * 2)
tickerDf['Lower'] = tickerDf['MA20'] - (tickerDf['20dSTD'] * 2)

# RSI
delta = tickerDf['Close'].diff()
window = 14
up_days = delta.copy()
up_days[delta<=0]=0.0
down_days = abs(delta.copy())
down_days[delta>0]=0.0
RS_up = up_days.rolling(window).mean()
RS_down = down_days.rolling(window).mean()
rsi= 100-100/(1+RS_up/RS_down)
tickerDf['RSI'] = rsi

# Create signals
tickerDf['Buy_Signal'] = (tickerDf['RSI'] < 30) & (tickerDf['Close'] < tickerDf['Lower'])
tickerDf['Sell_Signal'] = (tickerDf['RSI'] > 70) & (tickerDf['Close'] > tickerDf['Upper'])

# Plot
plt.figure(figsize=(12,5))
plt.grid(True)
plt.plot(tickerDf['Close'],label='Close Price', color='blue', alpha=0.35)
plt.plot(tickerDf['MA20'],label='Moving Average 20', color='red', alpha=0.35)
plt.fill_between(tickerDf.index, tickerDf['Lower'], tickerDf['Upper'], color='orange', alpha=0.1)
plt.scatter(tickerDf.index, tickerDf['Buy_Signal'] * tickerDf['Close'], color='green', label='Buy Signal', marker='^', alpha=1)
plt.scatter(tickerDf.index, tickerDf['Sell_Signal'] * tickerDf['Close'], color='red', label='Sell Signal', marker='v', alpha=1)
plt.legend(loc='best')
plt.show()
