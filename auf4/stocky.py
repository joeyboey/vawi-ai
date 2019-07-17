# %% Imports
import numpy as np
import pandas as pd
import json
import requests
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

# %% Data Loading & Preparation
symbol = 'AAPL'
data = pd.DataFrame.from_dict(json.loads(requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&outputsize=full&apikey=MQV0GEJOFA0VJXRS").text)["Time Series (Daily)"], orient="index").astype("float")
norm_data = data.apply(lambda x: x / x.iloc[0] - 1, axis=0)
print(norm_data[:5])
x_train, y_train = [norm_data.iloc[60:] for i in range(60, len(norm_data))], [norm_data[i] for i in range(60, len(norm_data))]
print(y_train)
