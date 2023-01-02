# library to fetch ticker values and other information of the stock
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def graph(stock):
    stock_name = yf.Ticker(stock)
    hist = stock_name.history(period='1y')
    fig = go.Figure(data=go.Scatter(x=hist.index, y=hist['Close'], mode='lines'))
    fig.show()

#   Latest stock recommendation by top analysts
def recommendation(stock_name):
    stock = yf.Ticker(stock_name)
    df = stock.recommendations  # loading df with stock recommendation  data frame
    rows_count = len(df.index)
    rows_count = rows_count - 1  # computing the last index in the data frame
    firm = df["Firm"][rows_count]  # extracting the name of the firm which gave the recommendation
    advise = df["To Grade"][rows_count]  # extracting the decision of the firm which gave the recommendation
    reco = firm + ' ' + advise  # concatenating the firm name and their advice
    return reco


# fetching closing prices for a particular stock and day
def get_closing(stock_name, day):
    stock = yf.Ticker(stock_name)
    data = stock.history(period=day)
    return data["Close"][0]


def averaging(name, days):
    total = 0
    sum_of_closing = 0
    for x in range(1, days + 1):    # iterating for each day as required by the accuracy
        num = str(x)
        day = num + 'd'     # concatenating the day number with 'd' : 1d , 2d ..
        v = get_closing(name, day)  # passing name of stock and the day into get_losing function
        sum_of_closing += v
        total += 1
    average = sum_of_closing / total    # averaging out closing prices to predict the next
    return average


# "scoring criteria " this will evaluate and advise the user whether he should , buy , keep or sell
def scoring(stock_name):
    score = 25
    stock = yf.Ticker(stock_name)

    df = stock.recommendations  # loading df with stock recommendation  data frame
    rows_count = len(df.index)
    rows_count = rows_count - 1  # computing the last index in the data frame
    advice = df["To Grade"][rows_count]
    closing_price = get_closing(stock_name, '1d')

    # add a trend variable here , so < 50% sell , 50% neutral , > 50% buy ???
    if advice == 'Buy' or advice == 'Overweight':
        score += 50
    elif advice == 'neutral':
        score += 25
    if closing_price > averaging(stock_name, 3):
        score += 25
    return score


# getting stock info (avg volume , market cap )
def info(stock_name):
    stock = yf.Ticker(stock_name)
    average_volume = stock.info['averageDailyVolume10Day']
    market_cap = stock.info["marketCap"]
    # returns it as a tuple
    return average_volume, market_cap


# drawing previous performance graph
def graph_prev(stock_name):
    stock = yf.Ticker(stock_name)
    df1 = pd.DataFrame(dict(
        x=[get_closing(stock, '7d'), get_closing(stock, '6d'), get_closing(stock, '5d'), get_closing(stock, '4d'),
           get_closing(stock, '3d'), get_closing(stock, '2d'), get_closing(stock, '1d')],
        y=[1, 3, 6, 4, 3, 7, 12, 6, 7]
    ))
    return df1


# drawing predicted graph
def graph_predicted(stock_name):
    stock = yf.Ticker(stock_name)
    df2 = pd.DataFrame(dict(
        x=[get_closing(stock, '7d'), get_closing(stock, '6d'), get_closing(stock, '5d'), get_closing(stock, '4d'),
           get_closing(stock, '3d'), averaging(stock_name, 3),
           get_closing(stock, '1d') + (averaging(stock_name, 3) / 5)],
        y=[1, 3, 6, 4, 3, 7, 12, 6, 7]
    ))
    return df2


# nasdaq , sandP and dow jones (if last close < average then red else green)
def index_fund():
    flag_1 = 0
    flag_2 = 0
    flag_3 = 0

    # vanguard s & p 500
    sandp = yf.Ticker("voo")
    van_close = sandp.history(period="1d")
    print(van_close["Close"][0])
    recent_close = sandp.info['previousClose']
    average_closing = sandp.info["fiftyDayAverage"]
    if recent_close > average_closing:
        flag_1 = 1    # flag 1 if green else 0 (red)

    # dow jones
    dj = yf.Ticker("djia")
    dj_close = dj.history(period="1d")
    print(dj_close["Close"][0])
    recent_close = dj.info['previousClose']
    average_closing = dj.info["fiftyDayAverage"]
    if recent_close > average_closing:
        flag_2 = 1  # flag 1 if green else 0 (red)

    # nasdaq
    nas = yf.Ticker("NDAQ")
    nas_close = nas.history(period="1d")
    print(nas_close["Close"][0])
    recent_close = nas.info['previousClose']
    average_closing = nas.info["fiftyDayAverage"]
    if recent_close > average_closing:
        flag_3 = 1  # flag 1 if green else 0 (red)

# flag_1 (color of s&p) , flag_2 (color of dow jones) , flag_3 (color of nasdaq)
    return van_close, flag_1, dj_close, flag_2, nas_close, flag_3
