import flet as ft
from flet import (LinearGradient, alignment, UserControl, Page, View,
                  LinearGradient,
                  UserControl,
                  Page,
                  Column,
                  Row,
                  Container,
                  Text,
                  padding,
                  alignment,
                  GridView,
                  transform,
                  animation,
                  TextField,
                  FilledTonalButton,
                  ButtonStyle,
                  SnackBar,
                  FilledButton,
                  Card)
from flet.plotly_chart import PlotlyChart
import plotly.express as px
import pandas as pd
import requests
import yfinance as yf
import webbrowser
import numpy as np
#import pandas_ta as ta
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from keras import optimizers
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, LSTM, Input, Activation, Dropout


# install packages kaleido, pyplotify, yfinance, flet, contourpy, pandas, numpy, plotly, matplotlib,

def main(page: ft.Page):
    username = "User"
    # Output for news list


    # Extra Info for indexes
    sandP = "S&P"
    sandPperc = 0.42
    sandPpoints = 3934.38
    nasdaq = "NASDAQ"
    nasdaqperc = -3.01
    nasdaqpoints = 6534.03
    dowjones = "DOW JONES"
    dowjonesperc = 4.67
    dowjonespoints = 2671.80

    # Previous performance data
    df1 = pd.DataFrame(dict(
        x=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        y=[1, 3, 6, 4, 3, 7, 12, 6, 7]
    ))
    # Predicted performance data
    df2 = pd.DataFrame(dict(
        x=[1, 2, 3, 4, 5, 6, 7, 8],
        y=[1, 3, 5, 4, 9, 6, 3, 2]
    ))
    # current stock details
    recommend = "Buy"
    opiniontext = "BLMBRG - BUY UBS - SELL M&P - BUY"
    avgvolumetext = 83.30
    marketcaptext = 2260
    cpricetext = 142.5
    ppricetext = 150
    stockname = "AAPL"

    page.window_maximized = True
    widthself = page.window_width
    heightself = page.window_height
    page.title = "StonkBot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#030315"
    page.theme = ft.Theme(font_family="SF Pro")
    theme = ft.Theme()
    theme.page_transitions.windows = "cupertino"
    page.theme = theme
    page.update()
    snack = SnackBar(
        Text("Registration successful!")
    )

    def GradientGenerator(start, end):
        ColorGradient = LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=[
                start,
                end,
            ],
        )

        return ColorGradient

    def req_registter(e, email, password):
        data = {
            "email": email,
            "password": password,
        }
        res = requests.post("http://127.0.0.1:5000/register", json=data)

        if res.status_code == 201 or 1 == 1:
            snack.open = True
            page.update()
        else:
            snack.content.value = "You were not registered. Try again."
            snack.open = True
            page.update()

    def req_login(e, email, password):
        data = {
            "email": email,
            "password": password,
        }

        res = requests.post("http://127.0.0.1:5000/login", json=data)

        if (res.status_code == 201 or 1 == 1):
            page.go("/dash")
        else:
            snack.content.value = "Could not log in. Try again."
            snack.open = True
            page.update()

        page.update()

    page.update()

    class Dashboard(UserControl):

        # hover function setup
        def hover_animation(self, e):
            if e.data == "true":
                e.control.content.controls[2].offset = transform.Offset(0, 0)
                e.control.content.controls[2].opacity = 100
                e.control.update()
            else:
                e.control.content.controls[2].offset = transform.Offset(0, 1)
                e.control.content.controls[2].opacity = 0
                e.control.update()

        # main container
        def MainContainer(self):

            self.main = Container(
                width=1400,
                height=600,
                bgcolor='black',
                border_radius=35,
                padding=8,
            )

            # main column
            self.main_col = Column()

            self.green_container = Container(
                width=self.main.width,
                height=self.main.height * 0.3569660112501453,
                border_radius=30,
                gradient=LinearGradient(
                    begin=alignment.top_left,
                    end=alignment.bottom_right,
                    colors=["#667eea", "#764ba2"],
                ),
            )

            self.inner_green_container = Container(
                width=self.green_container.width,
                height=self.green_container.height,
                content=Row(
                    spacing=0,
                    controls=[
                        Column(
                            expand=4,
                            controls=[
                                Container(
                                    padding=20,
                                    expand=True,
                                    content=Row(
                                        controls=[
                                            Column(
                                                controls=[
                                                    Text(
                                                        "WELCOME BACK",
                                                        size=15,
                                                        color='white70',
                                                    ),
                                                    Text(
                                                        "User",
                                                        size=30,
                                                        color='white7',
                                                        weight="bold",
                                                    ),
                                                    Row(
                                                        spacing=20,
                                                        controls=[
                                                            FilledTonalButton(
                                                                content=Text(
                                                                    "Go To Search",
                                                                    weight="w700",
                                                                ),
                                                                width=180,
                                                                height=40,
                                                                on_click=lambda _: page.go("/main"),
                                                            ),

                                                        ],
                                                    ),FilledTonalButton(
                                                        content=Text(
                                                            "Transaction Log",
                                                            weight="w700",
                                                        ),
                                                        width=180,
                                                        height=40,
                                                        on_click=lambda _: page.go("/transactionLog"),
                                                    ),
                                                ])]))])]))

            self.grid_news = GridView(
                expand=True,
                max_extent=301,
                runs_count=0,
                spacing=12,
                run_spacing=5,
                horizontal=True
            )

            # lower half
            self.main_content_area = Container(
                width=self.main.width,
                height=self.main.height * 0.5930339887498547,
                bgcolor="black",
                padding=padding.only(top=10, left=10, right=10),
                content=Column(
                    spacing=30,
                    controls=[
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="end",
                            controls=[
                                Container(
                                    content=Text(
                                        "Business News",
                                        size=25,
                                        weight="bold",
                                    )
                                ),
                                Container(
                                    content=Text(
                                        "view all",
                                        size=10,
                                        weight="w400",
                                        color="white54",
                                    ),
                                ),
                            ],
                        ),
                        self.grid_news,

                    ],
                ),
            )

            #

            news_list_data = [
                ["Apple", "The Wall Street Journal"],
                ["Microsoft", "The Wall Street Journal"],
                ["Tesla", "The Wall Street Journal"],
                ["Apple", "Forbes"],
                ["Best Performing Stock", "Forbes"],
                ["Market Overview", "NY Times"], ]

            news_list = news_list_data

            news_url = [
                "https://www.wsj.com/market-data/quotes/AAPL",
                "https://www.wsj.com/market-data/quotes/MSFT",
                "https://www.wsj.com/market-data/quotes/TSLA",
                "https://www.forbes.com/companies/apple/",
                "https://www.forbes.com/advisor/au/investing/best-stocks-to-buy-now/",
                "https://www.nytimes.com/section/markets-overview",
            ]

            def on_click(url: str):
                def handler(e: ft.ContainerTapEvent):
                    webbrowser.open(url)

                return handler

            for i, news_item in enumerate(news_list):
                url = news_url[i] if i < len(news_url) else ""  # Use URL if available, else empty string
                container = Container(
                    width=10,
                    height=10,
                    bgcolor="white10",
                    border_radius=15,
                    alignment=alignment.center,
                    content=Text(f"{news_item}", weight="bold"),
                    on_hover=lambda e: self.hover_animation(e),
                    on_click=on_click(url),
                )
                self.grid_news.controls.append(container)

                # Assuming you intended to iterate over news_item, not i
                for x in news_item:
                    container.content = Column(
                        alignment='center',
                        horizontal_alignment="center",
                        controls=[
                            Text(f"{news_item[1]}", size=11, color="white54"),
                            Text(f"{news_item[0]}", size=16, weight="bold"),
                            Text(
                                "See full story",
                                color="white60",
                                size=12,
                                text_align="start",
                                weight="w600",
                                offset=transform.Offset(0, 1),
                                animate_offset=animation.Animation(
                                    duration=900, curve="decelerate"
                                ),
                                animate_opacity=300,
                                opacity=0,
                            )
                        ],
                    )

            self.grid_news.controls.append(container)

            self.green_container.content = self.inner_green_container

            self.main_col.controls.append(self.green_container)
            self.main_col.controls.append(self.main_content_area)

            self.main.content = self.main_col

            return self.main

        def build(self):
            return Column(
                controls=[
                    self.MainContainer(),
                ]
            )

    app2 = Dashboard()
    page.update()

    # Updates the thing:
    def stockupdater(e):

        # -------------------------------------------------

        # -------------------------------------------------

        # -------------------------------------------------

        #   Latest stock recommendation by top analysts
        def recommendation(stock_name):
            stock = yf.Ticker(stock_name)
           #  df = stock.recommendations  # loading df with stock recommendation  data frame
           # rows_count = len(df.index)
           # rows_count = rows_count - 1  # computing the last index in the data frame
            # firm = df["Firm"][rows_count]  # extracting the name of the firm which gave the recommendation
            # advise = df["To Grade"][rows_count]  # extracting the decision of the firm which gave the recommendation
            # reco = firm + ' ' + advise  # concatenating the firm name and their advice
            return "Buy"

        # fetching closing prices for a particular stock and day
        def get_closing(stock_name, day):
            stock = yf.Ticker(stock_name)
            data = stock.history(period=day)
            return data["Close"][0]

        def averaging(name, days):
            total = 0
            sum_of_closing = 0
            for x in range(1, days + 1):  # iterating for each day as required by the accuracy
                num = str(x)
                day = num + 'd'  # concatenating the day number with 'd' : 1d , 2d ..
                v = get_closing(name, day)  # passing name of stock and the day into get_losing function
                sum_of_closing += v
                total += 1
            average = sum_of_closing / total  # averaging out closing prices to predict the next
            return average

        # "scoring criteria " this will evaluate and advise the user whether he should , buy , keep or sell
        def scoring(stock_name):
            score = 25
            stock = yf.Ticker(stock_name)

            #  df = stock.recommendations  # loading df with stock recommendation  data frame
             # rows_count = len(df.index)
             # rows_count = rows_count - 1  # computing the last index in the data frame
            # advice = df["To Grade"][rows_count]
            closing_price = get_closing(stock_name, '1d')

            # add a trend variable here , so < 50% sell , 50% neutral , > 50% buy ???
            if advice == 'Buy' or advice == 'Overweight' or 1 == 1:
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
            stock = (stock_name)

            current_date = dt.datetime.now().strftime('%Y-%m-%d')

            company = stock
            training_start = '2012-8-1'  # TRAINING::: for decade: start='2012-8-1', end='2022-12-3'  # for 2 months: start='2022-10-1', end='2022-12-3' (readibility purposes)
            training_end = '2022-12-3'
            prediction_days = 30
            test_start = dt.datetime(2020, 1, 1)
            test_end = dt.datetime.now()
            # Decrease prediction_days from 30 to 5 and time range from a decade to 2 months for readability purposes

            # Download Stock Data
            data = yf.download(tickers=company, start=training_start,
                               end=training_end)  # for decade: start='2012-8-1', end='2022-12-3'  # for 2 months: start='2022-10-1', end='2022-12-3'

            print(f"Downloaded {company} Stock Data for {training_start} to {training_end}:\n", data)
            print(
                "_______________________________________________________________________________________________________________")

            # Scaling Closing Price of Stock Data
            scaler = MinMaxScaler(feature_range=(0, 1))  # List of Closing prices
            scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))  # weighted between 0 and 1

            print("Closing Price as Scaled Data:\n", scaled_data)
            print(
                "_______________________________________________________________________________________________________________")

            # Filling Data into Training Input and Training Output
            # How many days do we want to look in the past to predict the future?
            training_input = []  # eg: [for i=1], x_train => [0.5529 0.5817 0.2799] (Values in the past)
            training_output = []  # eg: [for i=1], y_train => [0.3795] (Value to predict)

            for x in range(prediction_days, len(scaled_data)):
                training_input.append(scaled_data[x - prediction_days:x, 0])
                training_output.append(scaled_data[x, 0])

            print("training_input\t\t\t\t\t\t\t\t\t\t\t\t\t\ttraining_output")
            print("Past 3 values:\t\t\t\t\t\t\t\t\t\t\t\t\tValue to Predict:")
            for i, j in zip(training_input, training_output):
                print(f"{i}\t\t {j}")
            print(
                "_______________________________________________________________________________________________________________")

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
            print(
                "_______________________________________________________________________________________________________________")

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
            print(
                "_______________________________________________________________________________________________________________")

            # Make Predictions on Test Data

            x_test = []

            for x in range(prediction_days, len(model_inputs)):
                x_test.append(model_inputs[x - prediction_days:x, 0])

            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            print("Model Test Input 2:\n ", x_test)
            print(
                "_______________________________________________________________________________________________________________")

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

            df1 = pd.DataFrame(dict(
                x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                   28, 29, 30],
                y=[int(get_closing(stock, '30d')), int(get_closing(stock, '29d')), int(get_closing(stock, '28d')),
                   int(get_closing(stock, '27d')), int(get_closing(stock, '26d')), int(get_closing(stock, '25d')),
                   int(get_closing(stock, '24d')), int(get_closing(stock, '23d')), int(get_closing(stock, '22d')),
                   int(get_closing(stock, '21d')), int(get_closing(stock, '20d')), int(get_closing(stock, '19d')),
                   int(get_closing(stock, '18d')), int(get_closing(stock, '17d')), int(get_closing(stock, '16d')),
                   int(get_closing(stock, '15d')), int(get_closing(stock, '14d')), int(get_closing(stock, '13d')),
                   int(get_closing(stock, '12d')), int(get_closing(stock, '11d')), int(get_closing(stock, '10d')),
                   int(get_closing(stock, '9d')), int(get_closing(stock, '8d')), int(get_closing(stock, '7d')),
                   int(get_closing(stock, '6d')), int(get_closing(stock, '5d')), int(get_closing(stock, '4d')),
                   int(get_closing(stock, '3d')), int(get_closing(stock, '2d')), int(get_closing(stock, 'd'))], ))



            return df1, predictions

        # drawing predicted graph
        def graph_predicted(stock_name, predictions):
            predictions = predictions.flatten()
            stock = (stock_name)
            df2 = pd.DataFrame(dict(
                x=[1, 2, 3, 4, 5],
                y=[predictions[0], predictions[1], predictions[2],
                   predictions[3],
                   predictions[4]],

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
                flag_1 = 1  # flag 1 if green else 0 (red)

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


        # Page Properties:
        stockname = stocksearch.value
        # Previous performance data
        df1, predictionss = graph_prev(stockname)
        # Predicted performance data
        df2 = graph_predicted(stockname, predictionss)
        # current stock details
        score = 50
        if score > 50:
            recommend = "Buy"
        else:
            recommend = "Sell"
        opiniontext = recommendation(stockname)
        avgvolumetext, marketcaptext = info(stockname)
        cpricetext = get_closing(stockname, "1d")
        ppricetext = averaging(stockname, 5)

        recommendation = ft.Text("Recommendation: " + str(recommend), text_align=ft.TextAlign.CENTER, size=30,
                                 color=ft.colors.GREEN if recommend == "Buy" else ft.colors.RED,
                                 font_family="Roboto", weight=ft.FontWeight.BOLD)
        opinions = ft.Text("Other Opinions: " + opiniontext, text_align=ft.TextAlign.CENTER, size=20,
                           color=ft.colors.WHITE70, font_family="Open Sans Regular", )
        avg_volume = ft.Text("Average Volume: " + str(avgvolumetext), text_align=ft.TextAlign.CENTER, size=20,
                             color=ft.colors.WHITE70, font_family="Open Sans Regular", )
        marketcap = ft.Text("Market Cap: " + str(marketcaptext), text_align=ft.TextAlign.CENTER, size=20,
                            color=ft.colors.WHITE70, font_family="Open Sans Regular", )
        currentprice = ft.Text("Current Price: $" + str(cpricetext), text_align=ft.TextAlign.CENTER, size=20,
                               color=ft.colors.WHITE70, font_family="Open Sans Regular", )
        predictedprice = ft.Text("Predicted Price: ~$" + str(ppricetext), text_align=ft.TextAlign.CENTER, size=20,
                                 color=ft.colors.WHITE70, font_family="Open Sans Regular", )

        # Header Containers
        stockcolumn = ft.Column([ft.Container(
            content=ft.Text(stockname, text_align=ft.TextAlign.CENTER, size=30,
                            color=ft.colors.WHITE, font_family="Google Sans", ),
            bgcolor=ft.colors.BLACK,
            width=120, border=ft.border.all(0.5, ft.colors.BLUE_ACCENT),
            height=48,
            border_radius=10,
        ), ])
        usercolumn = ft.Column([ft.Container(
            content=ft.Row([ft.Text(username, size=30,
                                    color=ft.colors.WHITE,
                                    font_family="SF Pro", ), ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE_SHARP,
                                                                           icon_color=ft.colors.WHITE, icon_size=32,
                                                                           on_click=lambda _: page.go("/dash"), ), ],
                           alignment=ft.MainAxisAlignment.END, spacing=0),
            height=48, padding=ft.padding.only(left=16, right=7),
            border_radius=10,
            border=ft.border.all(1.5, ft.colors.BLACK),
            gradient=LinearGradient(
                begin=alignment.top_left,
                end=alignment.bottom_right,
                colors=["#667eea", "#764ba2"]
            )
        ), ])

        # Graphs For Stock
        fig1 = px.line(df1, x="x", y="y")
        fig1.update_layout(template='plotly_dark', title="Previous Performance",
                           xaxis_title="Time",
                           yaxis_title="Stock Price", width=1050,
                           height=500)

        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)")

        fig2 = px.line(df2, x="x", y="y")
        fig2.update_layout(template='plotly_dark', title="Predicted Performance",
                           xaxis_title="Time",
                           yaxis_title="Stock Price", width=1050,
                           height=500, )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)")
        if recommend == "Buy":
            fig2.update_traces(line_color='green')
        else:
            fig2.update_traces(line_color='red')

        # Payment Button interaction
        def btn_click(e):
            payment.controls.append(ft.Text(f"Payment Processed"))
            page.update()
            credit_card.focus()

        # Third Row Columns
        infocolumn = ft.Column([recommendation, opinions, avg_volume, marketcap, currentprice, predictedprice])
        infostockcolumn = ft.Column([sandpinfolabel, nasdaqinfolabel, dowjonesinfolabel])
        paymentcolumn = ft.Column([
            credit_card,
            cvv,
            card_name,
            ft.ElevatedButton("Purchase Stock", on_click=btn_click),
            payment, ])

        # For Final Output to page:
        # Rows Arrangements
        first_row = ft.Row([usercolumn, stockcolumn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        second_row = ft.Row([
            ft.Container(
                content=PlotlyChart(fig1, expand=True),
                margin=1,
                padding=1, border=ft.border.all(0.7, ft.colors.BLUE),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLACK,
                width=0.51 * widthself,  # 665
                height=0.42 * heightself,  # 320
                border_radius=10,
            ),
            ft.Container(
                content=PlotlyChart(fig2, expand=True),
                margin=1,
                padding=1,
                border=ft.border.all(0.7, ft.colors.GREEN) if recommend == "Buy" else ft.border.all(0.7,
                                                                                                    ft.colors.RED),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLACK,
                width=0.51 * widthself,  # 665
                height=0.42 * heightself,  # 320
                border_radius=10,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        third_row = ft.Row([ft.Container(
            content=infocolumn,
            margin=1, padding=ft.padding.symmetric(vertical=10, horizontal=25),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK,
            border=ft.border.all(1, ft.colors.GREEN) if recommend == "Buy" else ft.border.all(0.8, ft.colors.RED),
            border_radius=10, height=290, width=0.43 * widthself
        ), ft.Container(
            content=infostockcolumn,
            margin=1,
            padding=10, border=ft.border.all(0.8, ft.colors.BLUE),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK,
            border_radius=10, width=352, height=290
        ), ft.Container(
            content=paymentcolumn,
            margin=1,
            padding=10, border=ft.border.all(0.8, ft.colors.WHITE),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK,
            border_radius=10, height=290, width=0.31 * widthself
        )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        main_column2 = ft.Column([first_row, second_row, third_row])

        page.update()
        page.views.append(
            View(
                controls=[ft.Container(content=main_column2,
                                       border_radius=10, width=1990,
                                       bgcolor=ft.colors.BLACK,
                                       padding=ft.padding.symmetric(vertical=10, horizontal=10), )],
            )
        )
        page.update()

    page.update()

    # Text Info
    stocksearch = ft.TextField(label="Which stock do you want to look up?",
                               border=ft.InputBorder.NONE, border_radius=10, bgcolor=ft.colors.TRANSPARENT,
                               border_color=ft.colors.TRANSPARENT,
                               text_size=20, text_align=ft.TextAlign.LEFT)
    credit_card = ft.TextField(label="Enter Card Number", autofocus=False, text_align=ft.TextAlign.LEFT,
                               width=390, can_reveal_password=True, password=True)
    cvv = ft.TextField(label="Enter CVV", text_align=ft.TextAlign.LEFT, width=390)
    card_name = ft.TextField(label="Enter Name", text_align=ft.TextAlign.LEFT, width=390)
    payment = ft.Column()
    recommendation = ft.Text("Recommendation: " + str(recommend), text_align=ft.TextAlign.CENTER, size=30,
                             color=ft.colors.GREEN if recommend == "Buy" else ft.colors.RED,
                             font_family="Roboto", weight=ft.FontWeight.BOLD)
    opinions = ft.Text("Other Opinions: " + opiniontext, text_align=ft.TextAlign.CENTER, size=20,
                       color=ft.colors.WHITE70, font_family="Open Sans Regular", )
    avg_volume = ft.Text("Average Volume: " + str(avgvolumetext) + "M", text_align=ft.TextAlign.CENTER, size=20,
                         color=ft.colors.WHITE70, font_family="Open Sans Regular", )
    marketcap = ft.Text("Market Cap: " + str(marketcaptext) + "B", text_align=ft.TextAlign.CENTER, size=20,
                        color=ft.colors.WHITE70, font_family="Open Sans Regular", )
    currentprice = ft.Text("Current Price: $" + str(cpricetext), text_align=ft.TextAlign.CENTER, size=20,
                           color=ft.colors.WHITE70, font_family="Open Sans Regular", )
    predictedprice = ft.Text("Predicted Price: ~$" + str(ppricetext), text_align=ft.TextAlign.CENTER, size=20,
                             color=ft.colors.WHITE70, font_family="Open Sans Regular", )

    # Payment Button interaction
    def btn_click(e):
        payment.controls.append(ft.Text(f"Payment Processed"))
        page.update()
        credit_card.focus()

    # Favorites bar
    favorites_bar = ft.Row([
        ft.FilledTonalButton(content=ft.Text("Favorite 1", weight="w700"), on_click=lambda _: handle_favorite(1)),
        ft.FilledTonalButton(content=ft.Text("Favorite 2", weight="w700"), on_click=lambda _: handle_favorite(2)),
        ft.FilledTonalButton(content=ft.Text("Favorite 3", weight="w700"), on_click=lambda _: handle_favorite(3)),
        # Add more favorites as needed
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=15)

    # Header Containers
    usercolumn = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK_SHARP,
                              icon_color=ft.colors.WHITE, icon_size=32,
                              on_click=lambda _: page.go("/dash")),
                ft.Text(username, size=30, color=ft.colors.WHITE, font_family="SF Pro"),
                ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE_SHARP,
                              icon_color=ft.colors.WHITE, icon_size=32,
                              on_click=lambda _: page.go("/user_profile")),
            ], alignment=ft.MainAxisAlignment.END, spacing=0),
            height=48,
            padding=ft.padding.only(left=16, right=7),
            border_radius=10,
            border=ft.border.all(1.5, ft.colors.BLACK),
            gradient=LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#667eea", "#764ba2"]
            )
        ),
    ])

    # Stock column
    stockcolumn = ft.Column([
        ft.Container(
            content=ft.Text(stockname, text_align=ft.TextAlign.CENTER, size=30,
                            color=ft.colors.WHITE, font_family="Google Sans"),
            bgcolor=ft.colors.BLACK,
            width=120,
            border=ft.border.all(0.5, ft.colors.BLUE_ACCENT),
            height=48,
            border_radius=10,
        ),
    ])

    # Stock search column with added favorites bar
    stocksearchcolumn = ft.Container(
        content=ft.Row([
            usercolumn,
            ft.Row([stocksearch, ft.FilledTonalButton(content=ft.Text("Search", weight="w700"), on_click=stockupdater)],
                   spacing=15),
            favorites_bar,
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        bgcolor=ft.colors.BLACK,
        border_radius=30,
    )

    # Corrected order for the first_row
    first_row = ft.Row([stocksearchcolumn, stockcolumn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    #--------------------------1-1-1--1-1-1-1-1--1-1-1-1-----11--1-1-1-1--1-1-1-1-1-1-1--1-1-1
    # Graphs For Stock
    fig1 = px.line(df1, x="x", y="y")
    fig1.update_layout(template='plotly_dark', title="Previous Performance",
                       xaxis_title="Time",
                       yaxis_title="Stock Price", width=1050,
                       height=500)

    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)")

    fig2 = px.line(df2, x="x", y="y")
    fig2.update_layout(template='plotly_dark', title="Predicted Performance",
                       xaxis_title="Time",
                       yaxis_title="Stock Price", width=1050,
                       height=500, )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)")
    if recommend == "Buy":
        fig2.update_traces(line_color='green')
    else:
        fig2.update_traces(line_color='red')

    # Stock Index Containers
    if sandPperc > 0:
        sandpinfolabel = ft.Container(
            content=ft.Row([ft.Icon(name=ft.icons.ARROW_CIRCLE_UP_SHARP, color=ft.colors.GREEN, size=40), ft.Column([
                ft.Text(
                    sandP + "                  " + str(
                        sandPperc) + "%",
                    size=25,
                    color=ft.colors.GREEN,
                    font_family="SF Pro",
                    text_align=ft.TextAlign.START,
                    weight=ft.FontWeight.BOLD),
                ft.Text(
                    str(sandPpoints),
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    color=ft.colors.WHITE,
                    font_family="SF Pro", )], spacing=0)])
            ,
            border_radius=10, width=352, height=83,
            bgcolor=ft.colors.BLACK, padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border=ft.border.all(1, ft.colors.GREEN), )
    else:
        sandpinfolabel = ft.Container(
            content=ft.Row([
                ft.Icon(name=ft.icons.ARROW_CIRCLE_DOWN_SHARP, color=ft.colors.RED, size=40),
                ft.Column([
                    ft.Text(sandP + "                  " + str(sandPperc) + "%", size=25, color=ft.colors.RED,
                            font_family="SF Pro",
                            text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD),
                    ft.Text(str(sandPpoints), weight=ft.FontWeight.BOLD, size=18, color=ft.colors.WHITE,
                            font_family="SF Pro", )], spacing=0)])
            ,
            border_radius=10, width=352, height=83,
            bgcolor=ft.colors.BLACK, padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border=ft.border.all(1, ft.colors.RED), )

    if dowjonesperc > 0:
        dowjonesinfolabel = ft.Container(
            content=ft.Row([ft.Icon(name=ft.icons.ARROW_CIRCLE_UP_SHARP, color=ft.colors.GREEN, size=40), ft.Column([
                ft.Text(
                    dowjones + "     " + str(
                        dowjonesperc) + "%",
                    size=25,
                    color=ft.colors.GREEN,
                    font_family="SF Pro",
                    text_align=ft.TextAlign.START,
                    weight=ft.FontWeight.BOLD),
                ft.Text(
                    str(dowjonespoints),
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    color=ft.colors.WHITE,
                    font_family="SF Pro", )], spacing=0)])
            ,
            border_radius=10, width=352, height=83,
            bgcolor=ft.colors.BLACK, padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border=ft.border.all(1, ft.colors.GREEN), )
    else:
        dowjonesinfolabel = ft.Container(
            content=ft.Row([
                ft.Icon(name=ft.icons.ARROW_CIRCLE_DOWN_SHARP, color=ft.colors.RED, size=40),
                ft.Column([
                    ft.Text(dowjones + "     " + str(dowjonesperc) + "%", size=25, color=ft.colors.RED,
                            font_family="Abadi",
                            text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD),
                    ft.Text(str(dowjonespoints), weight=ft.FontWeight.BOLD, size=18, color=ft.colors.WHITE,
                            font_family="Abadi", )], spacing=0)])
            ,
            border_radius=10, width=352, height=83,
            bgcolor=ft.colors.BLACK, padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border=ft.border.all(1, ft.colors.RED), )

    if nasdaqperc > 0:
        nasdaqinfolabel = ft.Container(
            content=ft.Row([ft.Icon(name=ft.icons.ARROW_CIRCLE_UP_SHARP, color=ft.colors.GREEN, size=40), ft.Column([
                ft.Text(
                    nasdaq + "         " + str(
                        nasdaqperc) + "%",
                    size=25,
                    color=ft.colors.GREEN,
                    font_family="Abadi",
                    text_align=ft.TextAlign.START,
                    weight=ft.FontWeight.BOLD),
                ft.Text(
                    str(nasdaqpoints),
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    color=ft.colors.WHITE,
                    font_family="Abadi", )], spacing=0)])
            ,
            border_radius=10, width=352, height=83,
            bgcolor=ft.colors.BLACK, padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border=ft.border.all(1, ft.colors.GREEN), )
    else:
        nasdaqinfolabel = ft.Container(
            content=ft.Row([
                ft.Icon(name=ft.icons.ARROW_CIRCLE_DOWN_SHARP, color=ft.colors.RED, size=40),
                ft.Column([
                    ft.Text(nasdaq + "         " + str(nasdaqperc) + "%", size=25, color=ft.colors.RED,
                            font_family="Abadi",
                            text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD),
                    ft.Text(str(nasdaqpoints), weight=ft.FontWeight.BOLD, size=18, color=ft.colors.WHITE,
                            font_family="Abadi", )], spacing=0)])
            ,
            border_radius=10, width=352, height=83,
            bgcolor=ft.colors.BLACK, padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border=ft.border.all(1, ft.colors.RED), )

    # Third Row Columns
    infocolumn = ft.Column([recommendation, opinions, avg_volume, marketcap, currentprice, predictedprice])
    infostockcolumn = ft.Column([sandpinfolabel, nasdaqinfolabel, dowjonesinfolabel])
    paymentcolumn = ft.Column([
        credit_card,
        cvv,
        card_name,
        ft.ElevatedButton("Purchase Stock", on_click=btn_click),
        payment, ])

    # For Final Output to page:
    # Rows Arrangements
    first_row = ft.Row([usercolumn, stocksearchcolumn, stockcolumn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    second_row = ft.Row([
        ft.Container(
            content=PlotlyChart(fig1, expand=True),
            margin=1,
            padding=1, border=ft.border.all(0.7, ft.colors.BLUE),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK,
            width=0.51 * widthself,  # 665
            height=0.42 * heightself,  # 320
            border_radius=10,
        ),
        ft.Container(
            content=PlotlyChart(fig2, expand=True),
            margin=1,
            padding=1,
            border=ft.border.all(0.7, ft.colors.GREEN) if recommend == "Buy" else ft.border.all(0.7,
                                                                                                ft.colors.RED),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK,
            width=0.51 * widthself,  # 665
            height=0.42 * heightself,  # 320
            border_radius=10,
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    third_row = ft.Row([ft.Container(
        content=infocolumn,
        margin=1, padding=ft.padding.symmetric(vertical=10, horizontal=25),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        border=ft.border.all(1, ft.colors.GREEN) if recommend == "Buy" else ft.border.all(0.8, ft.colors.RED),
        border_radius=10, height=290, width=0.43 * widthself
    ), ft.Container(
        content=infostockcolumn,
        margin=1,
        padding=10, border=ft.border.all(0.8, ft.colors.BLUE),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        border_radius=10, width=352, height=290
    ), ft.Container(
        content=paymentcolumn,
        margin=1,
        padding=10, border=ft.border.all(0.8, ft.colors.WHITE),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        border_radius=10, height=290, width=0.31 * widthself
    )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    main_column = ft.Column([first_row, second_row, third_row])

    # ----------------------------------------------------------

    @staticmethod
    def TransactionLogContainer():
        # Assume you have a DataFrame with transaction data
        transaction_data = {
            'User ID': [1, 1, 2, 2],
            'Date': ['2023-01-01', '2023-01-05', '2023-01-02', '2023-01-06'],
            'Stock Ticker Bought': ['AAPL', 'MSFT', 'TSLA', 'GOOGL'],
            'Price at Purchase': [150.0, 200.0, 700.0, 2500.0],
            'Num of Shares Bought': [5, 3, 2, 1]
        }

        df = pd.DataFrame(transaction_data)

        # Create a flet Table from the DataFrame
        transaction_table = ft.Table.from_dataframe(df)

        return ft.Container(
            content=ft.Column([
                ft.Text("Transaction Log", size=25, weight="bold"),
                transaction_table
            ])
        )

    # ----------------------------------

    def route_change(route):

        email = TextField(
            label="Email",
            border="underline",
            width=320,
            text_size=14,
        )

        password = TextField(
            label="Password",
            border="underline",
            width=320,
            password=True,
            can_reveal_password=True,
        )

        page.views.clear()
        page.views.append(
            View(
                "/register",
                horizontal_alignment="center",
                vertical_alignment="center",
                controls=[
                    Column(
                        alignment="center",
                        controls=[
                            Card(
                                elevation=15,
                                content=Container(
                                    width=550,
                                    height=550,
                                    padding=padding.all(30),
                                    gradient=GradientGenerator("#1f2937", "#111827"),
                                    border_radius=ft.border_radius.all(12),
                                    content=Column(
                                        horizontal_alignment="center",
                                        alignment="start",
                                        controls=[
                                            Text(
                                                "Welcome to StonkBot📈",
                                                size=32,
                                                weight="w700",
                                                text_align="center",
                                            ),
                                            Text(
                                                "Enter a valid E-mail address, set a password, and get started!",
                                                size=14,
                                                weight="w700",
                                                text_align="center",
                                                color="#64748b",
                                            ),
                                            Text(
                                                "Already have an account? Login instead.",
                                                size=14,
                                                weight="w700",
                                                text_align="center",
                                                color="#ADD8E6",
                                            ),

                                            Container(padding=padding.only(bottom=20)),
                                            email,
                                            Container(padding=padding.only(bottom=10)),
                                            password,
                                            Container(padding=padding.only(bottom=20)),
                                            Row(
                                                alignment="center",
                                                spacing=20,
                                                controls=[
                                                    FilledButton(
                                                        content=Text(
                                                            "Register",
                                                            weight="w700",
                                                        ),
                                                        width=160,
                                                        height=40,
                                                        on_click=lambda e: req_registter(
                                                            e,
                                                            email.value,
                                                            password.value,
                                                        ),
                                                    ),
                                                    FilledButton(
                                                        content=Text(
                                                            "Login",
                                                            weight="w700",
                                                        ),
                                                        width=160,
                                                        height=40,
                                                        on_click=lambda __: page.go(
                                                            "/login"
                                                        ),
                                                    ),
                                                    snack,
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                            )
                        ],
                    )
                ],
            )
        )
        if page.route == "/login":
            page.views.append(
                View(
                    "/login",
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    controls=[
                        Column(
                            alignment="center",
                            controls=[
                                Card(
                                    elevation=15,
                                    content=Container(
                                        width=550,
                                        height=550,
                                        padding=padding.all(30),
                                        gradient=GradientGenerator(
                                            "#2f2937", "#251867"
                                        ),
                                        border_radius=ft.border_radius.all(12),
                                        content=Column(
                                            horizontal_alignment="center",
                                            alignment="start",
                                            controls=[
                                                Text(
                                                    "Welcome back!",
                                                    size=32,
                                                    weight="w700",
                                                    text_align="center",
                                                ),
                                                Text(
                                                    "We're so excited to see you again!",
                                                    size=14,
                                                    weight="w700",
                                                    text_align="center",
                                                    color="#64748b",
                                                ),
                                                Container(
                                                    padding=padding.only(bottom=20)
                                                ),
                                                email,
                                                Container(
                                                    padding=padding.only(bottom=10)
                                                ),
                                                password,
                                                Container(
                                                    padding=padding.only(bottom=20)
                                                ),
                                                Row(
                                                    alignment="center",
                                                    spacing=20,
                                                    controls=[
                                                        FilledButton(
                                                            content=Text(
                                                                "Login",
                                                                weight="w700",
                                                            ),
                                                            width=160,
                                                            height=40,
                                                            on_click=lambda e: req_login(
                                                                e,
                                                                email.value,
                                                                password.value,
                                                            ),
                                                        ),
                                                        FilledButton(
                                                            content=Text(
                                                                "Create account",
                                                                weight="w700",
                                                            ),
                                                            width=160,
                                                            height=40,
                                                            on_click=lambda __: page.go(
                                                                "/register"
                                                            ),
                                                        ),
                                                        snack,
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ),
                                )
                            ],
                        )
                    ],
                )
            )
        if page.route == "/dash":
            page.views.append(
                View(
                    "/dash",
                    [
                        app2,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        if page.route == "/main":
            page.views.append(
                View(
                    "/main",
                    [ft.Container(content=stocksearchcolumn,
                                  border_radius=10, width=1990,
                                  bgcolor=ft.colors.BLACK, padding=ft.padding.symmetric(vertical=10, horizontal=10), )],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        if page.route == "/transactionLog":
            page.views.append(
                View(
                    "/transactionLog",
                    content=TransactionLogContainer(),  # Assuming TransactionLogContainer is a valid function
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)

