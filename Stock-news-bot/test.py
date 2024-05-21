import requests
import smtplib

STOCK_NAME = "NQM"
COMPANY_NAME = "Nasdaq 100 index"

STOCKS_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY = "RBXQ0STH6IO0QZSQ"
NEWS_API_KEY = "2a045a67c21844d9a2cd0f33d630afc9"

my_email = "hawnyray@gmail.com"
my_password = "rjpitayimqtextjc"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY,
}

# Previous day closing price of the stock.

response = requests.get(STOCKS_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close_price = yesterday_data["4. close"]

# Day before yesterday closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# %difference in prices
dif = float(yesterday_close_price) - float(day_before_yesterday_closing_price)
up_down_sign = None
if dif > 0:
    up_down_sign = "🔺"
else:
    up_down_sign = "🔻"

price_percentage = ((dif / float(yesterday_close_price)) * 100)

if abs(price_percentage) < 1.5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    # Getting news from news API

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    news = articles[:1]
    formatted_email_body = [f"Headline: {article['title']}. Brief: {article['description']}" for article in news]

    # sending email
    try:
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs="zubkenny@gmail.com", msg=f'subject:{STOCK_NAME}'
                                                                                   f'{up_down_sign}{price_percentage}%'
                                                                                   f' \n\n {formatted_email_body}\n'
                                                                                   f'By @Zubby'.encode('utf-8'))

        connection.close()
        print("Email has been sent successfully!")
    except Exception as error:
        print(f"Error: {error}")

