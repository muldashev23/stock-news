import requests
import smtplib
import os
# Your email
MY_EMAIL = os.environ.get("EMAIL")
# Your email password
MY_PAS = os.environ.get("EmailPass")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
# ----------------- ALPHA VANTAGE API INFO ---------------------#
# Your API Key
API_KEY = os.environ.get("KEY_API")
API = "https://www.alphavantage.co/query"

# ----------------- NEWS API INFO ------------------------------#
# Your API key
NEWS_API_KEY = os.environ.get("NEWS_KEY_API")
NEWS_API = "https://newsapi.org/v2/everything"

# ----------------- ALPHA VANTAGE API PARAMETERS ---------------#

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": API_KEY
}

# ----------------- ALPHA VANTAGE DATA CODE -------------------#

response = requests.get(url=API, params=parameters)
data = response.json()["Time Series (Daily)"]
compare_data = [key for (key, value) in data.items()][:2]
today = data[compare_data[0]]
yesterday = data[compare_data[1]]
today_close = today["4. close"]
yesterday_close = yesterday["4. close"]


# ------------------ NEWS API PARAMETERS ----------------------#

news_parameters = {
    "q": COMPANY_NAME,
    "from": compare_data[0],
    "sortBy": "popularity",
    "language": "en",
    "apiKey": NEWS_API_KEY

}

# ------------------- NEWS API DATA CODE ----------------------#

response_news = requests.get(url=NEWS_API, params=news_parameters)
data_news = response_news.json()
list_of_news = data_news["articles"][:3]

# ------------------- COMPARE DAY CLOSES CODE -----------------#

differences = ((float(today_close) / float(yesterday_close)) - 1) * 100
if differences >= 4:
    for n in range(len(list_of_news)):
        title = list_of_news[n]['title']
        description = list_of_news[n]['description']
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PAS)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject:TSLA: UP{round(differences, 1)}%\n\n"
                                    f"Headline: {title}\n"
                                    f"{description}")
elif differences <= -4:
    for n in range(len(list_of_news)):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PAS)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject:TSLA: DOWN{round(differences, 1)}%\n\n"
                                    f"Headline: {list_of_news[n]['title']}\n"
                                    f"{list_of_news[n]['description']}")
