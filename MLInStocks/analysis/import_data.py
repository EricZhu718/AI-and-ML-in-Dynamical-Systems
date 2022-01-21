import time
import datetime
import pandas as pd
import yfinance as yf
import sys

def getDataFrame(start_date, end_date, ticker = '^GSPC'):
    data = yf.download(ticker, start_date, end_date).reset_index()
    return data.reset_index()


if __name__ == '__main__':
    print(getDataFrame('1990-01-01', '2021-07-12').filter(['Date', 'Open']))

    #frame = getDataFrame(input(), input(), input()).filter(['Date', 'Open'])
    #for line in frame.to_numpy():
    #    print(line)
    # print(frame)
    # print(frame.to_json())