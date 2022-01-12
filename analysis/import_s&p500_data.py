import time
import datetime
import pandas as pd
import yfinance as yf


def makeCSV(start_date, end_date):

    ticker = '^GSPC'
    data = yf.download(ticker, start_date, end_date)
    print(data)
    return data


if __name__ == '__main__':
    makeCSV('1990-01-01', '2021-07-12')

