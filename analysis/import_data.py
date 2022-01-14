import time
import datetime
import pandas as pd
import yfinance as yf


def getCSV(start_date, end_date, ticker = '^GSPC'):
    data = yf.download(ticker, start_date, end_date)
    print(data)
    return data.to_csv(index = False)


if __name__ == '__main__':
    print(getCSV('1990-01-01', '2021-07-12'))

