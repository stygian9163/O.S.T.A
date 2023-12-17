# Importing modules

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
#import pandas_ta as ta
import datetime as dt
import plotly.express as px

from sklearn.preprocessing import MinMaxScaler
from keras import optimizers
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, LSTM, Input, Activation, Dropout

# Defining parameters

current_date = dt.datetime.now().strftime('%Y-%m-%d')

company = 'MSFT'
training_start = '2012-8-1' # TRAINING::: for decade: start='2012-8-1', end='2022-12-3'  # for 2 months: start='2022-10-1', end='2022-12-3' (readibility purposes)
training_end = '2022-12-3'
prediction_days = 30
test_start = dt.datetime(2020, 1, 1)
test_end = dt.datetime.now()
# Decrease prediction_days from 30 to 5 and time range from a decade to 2 months for readability purposes

# Download Stock Data

data = yf.download(tickers=company, start=training_start, end=training_end)  # for decade: start='2012-8-1', end='2022-12-3'  # for 2 months: start='2022-10-1', end='2022-12-3'

print(f"Downloaded {company} Stock Data for {training_start} to {training_end}:\n", data)
print("_______________________________________________________________________________________________________________")



# Scaling Closing Price of Stock Data

scaler = MinMaxScaler(feature_range=(0, 1))                             # List of Closing prices
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))  # weighted between 0 and 1

print("Closing Price as Scaled Data:\n", scaled_data)
print("_______________________________________________________________________________________________________________")



# Filling Data into Training Input and Training Output
# How many days do we want to look in the past to predict the future?
training_input = []    # eg: [for i=1], x_train => [0.5529 0.5817 0.2799] (Values in the past)
training_output = []   # eg: [for i=1], y_train => [0.3795] (Value to predict)

for x in range(prediction_days, len(scaled_data)):
    training_input.append(scaled_data[x-prediction_days:x, 0])
    training_output.append(scaled_data[x, 0])

print("training_input\t\t\t\t\t\t\t\t\t\t\t\t\t\ttraining_output")
print("Past 3 values:\t\t\t\t\t\t\t\t\t\t\t\t\tValue to Predict:")
for i, j in zip(training_input, training_output):
    print(f"{i}\t\t {j}")
print("_______________________________________________________________________________________________________________")




# Reshaping Training Input and Training Output
training_input, training_output = np.array(training_input), np.array(training_output)
training_input = np.reshape(training_input, (training_input.shape[0], training_input.shape[1], 1))

print("Training inputs and outputs reshaped correctly:")
print("training_input\t\t\ttraining_output")
print("Past 3 values:\t\t\tValue to Predict:")
print("\n")
for i, j in zip(training_input, training_output):
    print(f"{i}\t\t {j}")
    print("\n")
print("_______________________________________________________________________________________________________________")





# Build Model
np.random.seed(10)  # Ensure same predicted price for same input data for every prediction

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(training_input.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))  # Prediction of the next closing value

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(training_input, training_output, epochs=25, batch_size=32)




# Load Test Data in Model

test_data = yf.download(company, start=test_start, end=test_end)
actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

print("Model Test Input 1:\n ", model_inputs)
print("_______________________________________________________________________________________________________________")





# Make Predictions on Test Data

x_test = []

for x in range(prediction_days, len(model_inputs)):
    x_test.append(model_inputs[x-prediction_days:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

print("Model Test Input 2:\n ", x_test)
print("_______________________________________________________________________________________________________________")

predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)





# Predict Next Day

real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs + 1), 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)
print("one day Pred: ", prediction)


# Predict Next 5 Days

real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs + 1), 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
predictions = []
for i in range(5):
    prediction = model.predict(real_data)
    predictions.append(prediction)
    real_data = np.append(real_data[:, 1:, :], prediction.reshape(1, 1, -1), axis=1)


predictions = np.array(predictions)
predictions = scaler.inverse_transform(predictions.reshape(predictions.shape[0], predictions.shape[2]))
print("5 day Pred: ", predictions)




print(predictions)
print(predictions[0])
predictions = predictions.flatten()
print(predictions[0])
predictions




stock = 'MSFT'

def get_closing(stock_name, day):
            stock = yf.Ticker(stock_name)
            data = stock.history(period=day)
            return data["Close"][0]

df1 = pd.DataFrame(dict(x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
                        y=[int(get_closing(stock, '30d')), int(get_closing(stock, '29d')), int(get_closing(stock, '28d')), int(get_closing(stock, '27d')), int(get_closing(stock, '26d')), int(get_closing(stock, '25d')), int(get_closing(stock, '24d')), int(get_closing(stock, '23d')), int(get_closing(stock, '22d')), int(get_closing(stock, '21d')), int(get_closing(stock, '20d')), int(get_closing(stock, '19d')), int(get_closing(stock, '18d')), int(get_closing(stock, '17d')), int(get_closing(stock, '16d')), int(get_closing(stock, '15d')), int(get_closing(stock, '14d')), int(get_closing(stock, '13d')), int(get_closing(stock, '12d')), int(get_closing(stock, '11d')), int(get_closing(stock, '10d')), int(get_closing(stock, '9d')), int(get_closing(stock, '8d')), int(get_closing(stock, '7d')), int(get_closing(stock, '6d')), int(get_closing(stock, '5d')), int(get_closing(stock, '4d')), int(get_closing(stock, '3d')), int(get_closing(stock, '2d')), int(get_closing(stock, 'd')), predictions[0], predictions[1], predictions[2], predictions[3], predictions[4]],))

print(df1)





# Create a new column 'color' based on the condition (x < 30)
df1['color'] = ['purple' if x <= 30 else ('green' if df1['y'].iloc[-1] > df1['y'].iloc[-2] else 'red') for x in df1['x']]

# Plot the DataFrame using plotly express
fig = px.line(df1, x='x', y='y', line_group='color', color='color',
              title='Line Plot with Different Colors',
              labels={'x': 'X-axis', 'y': 'Y-axis'},
              color_discrete_map={'purple': 'purple', 'green': 'green', 'red': 'red'})

# Show the plot
fig.show()


