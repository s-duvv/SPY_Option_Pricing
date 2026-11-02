import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from scipy.stats import norm

#Lookback window setup

def returns(index: str, lookback: int, today = date.today()): #Specify the index you want and the lookback window
    str_today = today.strftime("%Y-%m-%d")
    window = today - relativedelta(months = lookback)
    str_window = window.strftime("%Y-%m-%d")
    data = yf.download(index, start=str_window, end = str_today, auto_adjust=False)["Adj Close"][index]
    log_returns = np.log(data / data.shift(1)).dropna() # Drop the first value
    mean = np.mean(log_returns) # daily mean
    vol = np.std(log_returns) # daily vol
    
    annualized_mean = mean * 252
    annualized_vol = vol * np.sqrt(252)
    
    return data, annualized_mean, annualized_vol
spy_1, spy_1_mean, spy_1_vol = returns("SPY", 1) #we get the datafram, annualized mean and annualized volatility
spy_3, spy_3_mean, spy_3_vol = returns("SPY", 3)
spy_6, spy_6_mean, spy_6_vol = returns("SPY", 6)
spy_12, spy_12_mean, spy_12_vol = returns("SPY", 12)

print(type(spy_1_vol))

print(f"The (annualized) volatility over a 1 month lookback window is: {spy_1_vol}")
print(f"The (annualized) volatility over a 3 month lookback window is: {spy_3_vol}")
print(f"The (annualized) volatility over a 6 month lookback window is: {spy_6_vol}")
print(f"The (annualized) volatility over a 12 month lookback window is: {spy_12_vol}")
    


# Historical distribution
today = date.today()
str_today = today.strftime("%Y-%m-%d")
spy_hist = yf.download("SPY", start= "1993-12-31", end= str_today, auto_adjust=False)["Adj Close"]["SPY"]

log_returns_hist = np.log(spy_hist / spy_hist.shift(1)).dropna() 

#Graph setup
plt.figure(figsize=(10,5))
count, bins, _ = plt.hist(log_returns_hist, bins=100, density=True, alpha=0.6, color='skyblue', label='SPY dist')

mu = log_returns_hist.mean() #get Gaussian params
sigma = log_returns_hist.std()
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100) #Guassian dist
plt.plot(x, norm.pdf(x, mu, sigma), color='blue', linewidth=2, label=f'Normal dist ($\mu$={mu:.4f}, $\sigma$={sigma:.4f})')

plt.title('SPY Historical')
plt.xlabel('Daily Log Return')
plt.ylabel('Density')
plt.legend()
plt.grid(True)
plt.show()