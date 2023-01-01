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
from enum import unique
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import yfinance as yf


# add banner if stock not found and allow retry


# User Login Authentication:
# db = SQLAlchemy()
#
#
# def createUUID():
#     return uuid4().hex
#
#
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.String(32), unique=True, primary_key=True, default=createUUID)
#     email = db.Column(db.String(355), unique=True)
#     password = db.Column(db.String(), nullable=False)
#
#
# class AppConfiguration:
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = True
#     SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
#
#
# app = Flask(__name__)
# app.config.from_object(AppConfiguration)
# db.init_app(app)
#
#
# @app.route("/register", methods=["POST"])
# def RegisterUser():
#     user_data = request.get_json()
#     user = User(email=user_data["email"], password=user_data["password"])
#     db.session.add(user)
#     db.session.commit()
#     return "done", 201
#
#
# @app.route("/login", methods=["POST"])
# def LogIn():
#     email = request.json["email"]
#     password = request.json["password"]
#
#     user = User.query.filter_by(email=email).first()
#
#     if user is None:
#         return jsonify({"error: Invalid email"}), 401
#
#     if user.password != password:
#         return jsonify({"error: Invalid Password"}), 401
#
#     return jsonify({"OK": "Login successful"}), 201
#
#
# with app.app_context():
#     db.create_all()
#
# if __name__ == "__main__":
#     app.run(debug=False)


def main(page: ft.Page):
    username = "User"
    # Output for news list
    news_list_data = [
        ["Apple", "The Wall Street Journal"],
        ["Microsoft", "The New York Times"],
        ["Tesla", "Forbes"],
        ["Example ", "News Source"],
        ["Example Company", "News Source"],
        ["Example Company", "News Source"],
        ["Example Company", "News Source"],
        ["Example Company", "News Source"],
        ["Example Company", "News Source"], ]

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
    page.window_resizable = False
    widthself = page.window_width
    heightself = page.window_height
    page.title = "Stock Analysis"
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

    # def on_search_for_stock(e):
    #     global stocknameinternal
    #     if stocksearch.value:
    #         stocknameinternal = stocksearch.value
    #     else:
    #         stocknameinternal = stockname
    #     page.update()
    #     return stocknameinternal

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

        if res.status_code == 201:
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

        if res.status_code == 201:
            page.views.append(
                View(
                    f"/{email}",
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    controls=[
                        Column(
                            alignment="center",
                            horizontal_alignment="center",
                            controls=[
                                Text(
                                    "Successfully logged in!",
                                    size=44,
                                    weight="w700",
                                    text_align="center",
                                ),
                                Text(
                                    f"Login Information:\nEmail: {email}\nPassword: {password}",
                                    size=32,
                                    weight="w500",
                                    text_align="center",

                                ),
                                FilledButton(
                                    content=Text(
                                        "Go To Dashboard",
                                        weight="w700",
                                    ),
                                    width=160,
                                    height=40,
                                    on_click=lambda _: page.go("/dash"),
                                ),
                            ],
                        ),
                    ],
                )
            )

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
                                                        size=25,
                                                        color='white70',
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
                                                                height=40, on_click=lambda _: page.go("/main"),
                                                            ),
                                                        ],
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
                                        size=20,
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
            news_list = news_list_data

            for i in news_list:
                __ = Container(
                    width=10,
                    height=10,
                    bgcolor="white10",
                    border_radius=15,
                    alignment=alignment.center,
                    content=Text(f"{i}", weight="bold"),
                    on_hover=lambda e: self.hover_animation(e),
                )
                self.grid_news.controls.append(__)

                for x in i:
                    __.content = Column(
                        alignment='center',
                        horizontal_alignment="center",
                        controls=[
                            Text(f"{i[1]}", size=11, color="white54"),
                            Text(f"{i[0]}", size=16, weight="bold"),
                            #
                            Text(
                                "See full story",
                                color="white60",
                                size=12,
                                text_align="start",
                                weight="w600",
                                offset=transform.Offset(0, 1),  # play w this
                                animate_offset=animation.Animation(
                                    duration=900, curve="decelerate"
                                ),
                                animate_opacity=300,
                                opacity=0,
                            )
                        ],
                    )

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
                x=[1, 2, 3, 4, 5, 6, 7],
                y=[int(get_closing(stock, '7d')), int(get_closing(stock, '6d')), int(get_closing(stock, '5d')),
                   int(get_closing(stock, '4d')),
                   int(get_closing(stock, '3d')), int(get_closing(stock, '2d')), int(get_closing(stock, '1d'))],

            ))
            return df1

        # drawing predicted graph
        def graph_predicted(stock_name):
            stock = yf.Ticker(stock_name)
            df2 = pd.DataFrame(dict(
                x=[1, 2, 3, 4, 5, 6, 7],
                y=[int(get_closing(stock, '7d')), int(get_closing(stock, '6d')), int(get_closing(stock, '5d')),
                   int(get_closing(stock, '4d')),
                   int(get_closing(stock, '3d')), int(averaging(stock_name, 3)),
                   int(get_closing(stock, '1d') + (averaging(stock_name, 3) / 5))],

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

        # -------------------------------------------------

        # -------------------------------------------------

        # else:
        #    snack.content.value = "Could not log in. Try again."
        #   snack.open = True
        #  page.update()

        # -------------------------------------------------

        # Page Properties:
        stockname = stocksearch.value
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
        score = scoring(stockname)
        if score > 50:
            recommend = "Buy"
        else:
            recommend = "Sell"
        opiniontext = recommendation(stockname)
        avgvolumetext, marketcaptext = info(stockname)
        cpricetext = 142.5
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

        # Payment Button interaction (Maybe Add PopUp?)
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

    # Header Containers

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
    stockcolumn = ft.Column([ft.Container(
        content=ft.Text(stockname, text_align=ft.TextAlign.CENTER, size=30,
                        color=ft.colors.WHITE, font_family="Google Sans", ),
        bgcolor=ft.colors.BLACK,
        width=120, border=ft.border.all(0.5, ft.colors.BLUE_ACCENT),
        height=48,
        border_radius=10,
    ), ])
    stocksearchcolumn = ft.Container(
        content=ft.Row([usercolumn,stocksearch,
                        ft.FilledTonalButton(
                            content=Text(
                                "Search",
                                weight="w700", ),
                            on_click=stockupdater), ],
                       alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=15),
        bgcolor=ft.colors.BLACK,
        border_radius=10,
    )
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

    # Payment Button interaction (Maybe Add PopUp?)
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

    def route_change(route):
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
                                                "Welcome to StockApp",
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
                                                        on_click=lambda __: page.go(
                                                            "/login")
                                                        # lambda e: req_registter(e,email.value,password.value,),
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
                                                            on_click=lambda __: page.go(
                                                                "/dash"
                                                            ),
                                                            # lambda e: req_login(e, email.value,
                                                            # password.value, ),
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
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
