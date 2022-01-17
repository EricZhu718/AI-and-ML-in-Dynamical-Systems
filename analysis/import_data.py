import time
import datetime
import pandas as pd
import yfinance as yf
import sys

def getDataFrame(start_date, end_date, ticker = '^GSPC'):
    data = yf.download(ticker, start_date, end_date)
    return data


if __name__ == '__main__':
    # (getDataFrame('1990-01-01', '2021-07-12')).to_csv('csv data/testing.csv')
    print(getDataFrame(input(), input()).to_json())