import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Set the parameters for the simulation
num_simulations = 1000
num_days = 252   # Roughly the number of trading days in a year

# Fetch the stock data and calculate daily returns
ticker = 'AAPL'
data = yf.download(ticker, start='2010-1-1', end='2023-12-31')
returns = data['Close'].pct_change()

# Calculate the mean and standard deviation of returns
mu = returns.mean()
sigma = returns.std()

# Create an empty matrix to hold the end price data
end_prices = np.zeros((num_simulations, num_days+1))   # Corrected here

# Simulate the price trajectories
for simulation in range(num_simulations):
    price_series = [data['Close'][-1]]

    # Generate price series using geometric Brownian motion
    for day in range(num_days):
        price = price_series[-1] * (1 + np.random.normal(mu, sigma))
        price_series.append(price)

    end_prices[simulation, :] = price_series   # This should work fine now

# Plot the first 100 simulations
for simulation in range(100):
    plt.plot(end_prices[simulation, :])
plt.show()

# Print the mean end price
print("Expected price: ", np.mean(end_prices))

# Print the 5% quantile (i.e., the price is expected to be above this 5% of the time)
print("5% quantile: ", np.percentile(end_prices, 5))

# Print the 95% quantile (i.e., the price is expected to be below this 95% of the time)
print("95% quantile: ", np.percentile(end_prices, 95))