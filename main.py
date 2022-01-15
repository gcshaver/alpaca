from datetime import datetime, timedelta, timezone
import json

import pandas as pd
from plotly import graph_objs as go
import requests
import time

from config import *

TICKER = 'BTCUSD'
OVERLAPPING_PULL = 5
TIME_INTERVAL = '5Min'

def get_account_details():
    r = requests.get(HOST_URL + '/v2/account', headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY})

    return json.loads(r.content)

def post_order(symbol=None,qty=None,side=None,type=None,time_in_force=None):
    r = requests.post(HOST_URL + '/v2/orders',
                      headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY},
                      json={'symbol': symbol, 'qty': qty, 'side': side, 'type': type, 'time_in_force': time_in_force})
    return json.loads(r.content)


# def get_bars(symbol=None,start=None,end=None,feed='IEX',timeframe='1Min'):
#     r = requests.get('https://data.alpaca.markets/' + '/v2/stocks/' + symbol + '/bars',
#                       headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY},
#                       params={'timeframe': timeframe, 'start': start, 'end': end})
#     return json.loads(r.content)

def get_bars(symbol=None,start=None,end=None,exchanges='CBSE',timeframe=TIME_INTERVAL):
    r = requests.get('https://data.alpaca.markets/' + '/v1beta1/crypto/' + symbol + '/bars',
                      headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY},
                      params={'timeframe': timeframe, 'start': start, 'end': end, 'exchanges': exchanges})
    return json.loads(r.content)

def get_current_minute():
    current_minute = datetime.now(timezone.utc).replace(second=0,microsecond=0)
    return current_minute

def subtract_time(base_time=None, seconds=0, minutes=0, hours=0, days=0):
    delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
    return (base_time - delta)

def datetime_format(timestamp=None):
    return timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

def create_bar_frame(bar_response):
    bar_dataframe = pd.DataFrame.from_records(data=bar_response['bars'])
    return bar_dataframe

def create_candlestick_chart(prices=None):
    fig = go.Figure(data=[go.Candlestick(x=prices.index,
                                         open=prices['o'],
                                         high=prices['h'],
                                         low=prices['l'],
                                         close=prices['c'])])
    fig.show()


def run():
    while True:
        current_time = get_current_minute()
        print('fetching latest market data for {} at {}'.format(TICKER, current_time))
        # latest_data_df = create_bar_frame(get_bars(symbol=TICKER, start=subtract_time(current_time, minutes=5)))
        historic_df = create_bar_frame(get_bars(TICKER)).set_index('t', drop=True)
        historic_df['SMA30'] = historic_df['c'].rolling(30).mean()
        print(historic_df)
        # historic_df.plot(x='t', y=['c', 'SMA30'], kind='line')
        # plt.show()
        create_candlestick_chart(prices=historic_df)
        # , x='t', y=['c', 'SMA30'], kind='line')
        print('sleeping 60s')
        time.sleep(60)

    






# print(get_account_details())
# posted_order = post_order(TICKER, '2', 'buy', 'market', 'day')
# print(posted_order)
# print(get_account_details())
# create_bar_frame(get_bars(symbol=TICKER,start='2022-01-07T19:12:00Z',end='2022-01-07T19:17:00Z'))
# print(create_bar_frame(get_bars(TICKER)))
# print(datetime_format(get_current_minute()))
# print(datetime_format(subtract_time(base_time=get_current_minute(), minutes =5)))

# print(get_bars(TICKER))
run()
