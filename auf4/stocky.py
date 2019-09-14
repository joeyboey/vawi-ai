# %% Imports
import numpy as np
import pandas as pd
import json
import requests
import time
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.layers import Activation, Dense, Dropout
from keras.layers import CuDNNLSTM as LSTM
from keras import backend as K

# %% Constants
SYMBOL = 'MSFT'
STEPS = 60
EPOCHS = 10
OPTIMIZER = RMSprop()
LOSS = 'mse'
METRICS = ['accuracy']
HIDDEN_LAYERS = 0
NAME = f"lstm-{SYMBOL}-{STEPS}-steps-{LOSS}-loss-{METRICS[0]}-metrics-{HIDDEN_LAYERS}-hidden_layers-{int(time.time())}.hdf5"

# %% Data Loading, Normalisation, Reshaping & Splitting
input = pd.DataFrame.from_dict(json.loads(requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + SYMBOL + "&outputsize=full&apikey=MQV0GEJOFA0VJXRS").text)["Time Series (Daily)"], orient="index").astype("float")
# dropped = input.drop(["1. open", "2. high", "3. low", "5. volume"], axis=1)
data = input.apply(lambda x: x / x.iloc[0] - 1, axis=0)
x, y = np.array([data[i:i+STEPS].values for i in range(len(data)-STEPS)]), pd.DataFrame(data["4. close"].values[STEPS:])
split = int(len(x) * .9)
x_train, x_test, y_train, y_test = x[:split], x[split:], y[:split], y[split:]
print("Stock:\t\t\t{}\nSteps to look back:\t{}\nInput Data:\n{}\n\n\tTraining\tTest\nx:\t{}\t{}\ny:\t{}\t{}\n".format(SYMBOL, STEPS, input[:5], x_train.shape, x_test.shape, y_train.shape, y_test.shape))

# %% Keras Model
model = Sequential()
model.add(LSTM(units=STEPS, batch_input_shape=(None, STEPS, len(data.columns)), return_sequences=True))
model.add(Dropout(.2))
for x in range(HIDDEN_LAYERS - 1):
    model.add(LSTM(units=STEPS * 2, return_sequences=True))
    model.add(Dropout(.2))
model.add(LSTM(units=STEPS * 2, return_sequences=False))
model.add(Dropout(.2))
model.add(Dense(units=1))
model.add(Activation("linear"))
start = time.time()
model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=METRICS)
print("Compilation Time : {}\nModel:\n{}".format(time.time() - start, model.summary(), NAME))

# %% Training
history = model.fit(
    x_train,
    y_train,
    batch_size=int(STEPS/2),
    epochs=EPOCHS,
    validation_split=.10)

# %% Model Statistics
result = model.predict(x_test)
plt.plot(result, c='r')
# print(result.shape, y_test.shape)
plt.plot(y_test.values, c='g')
plt.show()

# %% Save Model
model.save("models/" + NAME)

# %% Plotting of Loss History
plt.plot(history.history['loss'])
