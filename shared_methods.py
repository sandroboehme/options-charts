import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
import time
from IPython.display import Markdown
import os.path
import random
import hashlib
import pdb


# I use black for BTC
contrast_colors = ['red', 'orange', 'green', 'purple', 'brown', 'pink', 'olive', 'cyan', 'grey'] # add more colors if needed
all_colors = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
colors = [color for color in all_colors if color not in contrast_colors] # all_colors without contrast colors
colors = contrast_colors + colors # make sure the contrast columns come first

from IPython.display import IFrame
def getTradingViewWidget(ticker="Coinbase:BTCUSD"):
    chart_id = "xxxxx"
    # Unfortunately that doesn't work
    # https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#timeframe
    # &timeframe={{from:1640995200,to:1643673600}}
    # &timeframe=%7Bfrom%3A1640995200%2Cto%3A1643673600%7D
    # As well as the inverval and probably other parameters
    src = f'''https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{chart_id}
    &symbol={ticker}&interval=D&hidesidetoolbar=1&symboledit=1&saveimage=0&toolbarbg=f1f3f6&studies=%5B%5D&style=1&timezone=UTC&timeframe=%7Bfrom%3A1640995200%2Cto%3A1643673600%7D"
    '''
    return IFrame(src, '100%', '600px')

def showPlainPriceChart(df, strike_prices):
    fig = go.Figure()
    min_price = 0
    max_price = 0
    for i, strike_price in enumerate(strike_prices):
        if f'option_{strike_price}_usd' in df.columns:
            df_strike = df[f'option_{strike_price}_usd']
            min_price = min(min_price, df_strike.min())
            max_price = max(max_price, df_strike.max())
            fig.add_trace(go.Scatter(x=df['timestamp'],
                                     y=df_strike,
                                     name=f'Option {strike_price}',
                                     yaxis='y',
                                     mode='lines+markers',
#                                     connectgaps=True,
                                     line=dict(color=colors[i])))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_usd'],
                             name='BTC',
                             yaxis='y',
                             line=dict(color="black")))

    range = [min(min_price, df['btc_usd'].min()), max(max_price, df['btc_usd'].max())]

    fig.update_layout(width=1300, height=800)
    fig.update_layout(title="Plain prices in USD", yaxis=dict(title='Prices in USD', range=range))
    #    fig.update_traces(connectgaps=False)
    fig.show()

class Config:
    def __init__(self, config_dict):
        self.__dict__.update(config_dict)

def getBTCCallInstrumentName(expiration, strike):
    instrument = 'BTC-' + expiration + '-' + str(strike) + '-C'
    return instrument

def getInstrumentJson(instrumentName):
    fileName = "option_data/" + instrumentName + ".json"
    if os.path.isfile(fileName):
        if os.path.getsize(fileName) > 5:
            df = pd.read_json(fileName)
            return pd.json_normalize(df.trades)
        else:
            return None
    else:
        print(f"Downloading to {fileName}.")
        url = f'https://history.deribit.com/api/v2/public/get_last_trades_by_instrument?instrument_name={instrumentName}&count=10000&include_old=true'

        response = requests.get(url)
        responseJson = json.loads(response.text)
        if "result" in responseJson:
            # Parse the JSON response
            result = responseJson['result']
            with open(fileName, 'w') as f:
                json.dump(result, f)
            return pd.json_normalize(result['trades'])
        else:
            print(f"No data from Deribit for {instrumentName}.")
            with open(fileName, 'w') as f:
                json.dump("", f)
            return None
    df = df.drop_duplicates(subset=['timestamp'])
    return df

def getBTCdataframe():
    btc_ohlc = pd.read_csv('bitstamp-btc-ohlc.csv')
    btc_ohlc['timestamp'] = pd.to_datetime(btc_ohlc['timestamp'], unit='s').dt.date
    btc_ohlc = btc_ohlc.loc[:, ['timestamp', 'close']].copy()
    btc_ohlc = btc_ohlc.rename({'close': 'btc_usd'}, axis=1)
#    btc_ohlc = btc_ohlc.set_index('timestamp')
    return btc_ohlc

def getOptionDataframe(expiration, strike):
    df = getInstrumentJson(getBTCCallInstrumentName(expiration, strike))
    if (df is None):
        return None
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms').dt.date
    df = df.loc[:, ['timestamp', 'price']].copy()
    df = df.drop_duplicates(subset=['timestamp'])
#    df = df.set_index('timestamp')
    #    df.index = pd.to_datetime(df.index)
#    df = df.sort_index(ascending=False)
    return df

def getMergedDataframe(config):
    merged_df = getOptionDataframe(config.expiration, config.strikes[0])
    if (merged_df is None):
        merged_df = pd.DataFrame(columns=['timestamp'])
#        merged_df = merged_df.set_index('timestamp')
    else:
        merged_df.rename({'price': f'option_{config.strikes[0]}_usd'}, axis=1, inplace=True)
    strikes_to_be_removed = []
    for i, strike_price in enumerate(config.strikes[1:]):
        dfStrike = getOptionDataframe(config.expiration, strike_price)
        if (dfStrike is None):
            strikes_to_be_removed.append(strike_price)
        else:
            dfStrike.rename({'price': f'option_{strike_price}_usd'}, axis=1, inplace=True)
            merged_df = pd.merge(merged_df, dfStrike, on='timestamp', how='outer')

    display("These strikes don't have any data:")
    display(strikes_to_be_removed)
    config.strikes = [strike for strike in config.strikes if strike not in strikes_to_be_removed]
    btc_ohlc = getBTCdataframe()

    # Join option prices with btc prices. Keep the rows that at least have an options prices.
    merged_df = pd.merge(btc_ohlc, merged_df, on='timestamp', how='right')

    for i, strike_price in enumerate(config.strikes):
        merged_df[f'option_{strike_price}_usd'] = merged_df[f'option_{strike_price}_usd'] * merged_df['btc_usd']
    merged_df = merged_df.sort_values('timestamp', ascending=False)
    merged_df = merged_df.round(2)
    return merged_df


def showOffsettedPriceChart(df, strike_prices):
    fig = go.Figure()

    min_price = df['btc_usd'].min()
    max_price = df['btc_usd'].max()
    for i, strike_price in enumerate(strike_prices):
        df_strike = df[f'option_{strike_price}_offsetted_usd']
        min_price = min(min_price, df_strike.min())
        max_price = max(max_price, df_strike.max())
        fig.add_trace(go.Scatter(x=df['timestamp'],
                                 y=df_strike,
                                 name=f'Option {strike_price}',
                                 yaxis='y',
                                 line=dict(color=colors[i])))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_usd'],
                             name='BTC',
                             yaxis='y',
                             line=dict(color="black")))

    range = [min(min_price, df['btc_usd'].min()), max(max_price, df['btc_usd'].max())]

    fig.update_layout(width=1300, height=800)

    fig.update_layout(title="Interpolated option prices moved to start at the same point as BTC to visualize the delta", yaxis=dict(title='Prices in USD', range=range))

    fig.show()

def shiftLinesToTheStartOfBTC(df_param, strike_prices):
    df = df_param.interpolate(method='linear')
    df_shifted = pd.DataFrame({'timestamp': df['timestamp'], 'btc_usd': df['btc_usd']})
    firstBTCprice = df.loc[df.index[-1], 'btc_usd']
    for i, strike_price in enumerate(strike_prices):
        firstOptionPrice = df.loc[df.index[-1], f'option_{strike_price}_usd']
        strike_offset = firstBTCprice - firstOptionPrice
        df_shifted[f'option_{strike_price}_offsetted_usd'] = df[f'option_{strike_price}_usd'] + strike_offset
#    df_shifted = df_shifted.drop_duplicates(subset=['timestamp'])
    return df_shifted

def getPriceChanges(df, strike_prices):
    dfNew = pd.DataFrame(df['timestamp'])
    dfNew = pd.concat([dfNew, df['btc_usd']], axis=1)
    #dfNew = dfNew.interpolate(method='linear')

    for i, strike_price in enumerate(strike_prices):
        strike_col = df[f'option_{strike_price}_usd']
        dfNew[f'option_{strike_price}_changed_usd'] = strike_col - strike_col.shift(-1)
        dfNew[f'option_{strike_price}_changed_percent'] = dfNew[f'option_{strike_price}_changed_usd'] / (df[f'option_{strike_price}_usd']/100)
    dfNew['btc_usd_changed_usd'] =  df['btc_usd'] - df['btc_usd'].shift(-1)
    dfNew['btc_usd_changed_percent'] = dfNew['btc_usd_changed_usd'] / (df['btc_usd']/100)
    return dfNew

def plotOptionPricesChangedUSD(df, strikes):

    fig = go.Figure()

    for i, strike in enumerate(strikes):
        fig.add_trace(go.Scatter(x=df['timestamp'],
                                 y=df[f'option_{strike}_changed_usd'],
                                 name=f'Option {strike}', yaxis='y',
                                 line=dict(color=colors[i % len(colors)])))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_usd_changed_usd'],
                             name='BTC', yaxis='y',
                             line=dict(color='black')))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_usd'],
                             name='BTC price in USD on separate axis', yaxis='y2',
                             line=dict(color='gold')))

    range = [min([df[f'option_{strike}_changed_usd'].min() for strike in strikes] + [df['btc_usd_changed_usd'].min()]),
             max([df[f'option_{strike}_changed_usd'].max() for strike in strikes] + [df['btc_usd_changed_usd'].max()])]

    fig.update_layout(width=1600, height=800)
    fig.update_layout(title="Absolute changes in USD vs BTC price",
                      yaxis=dict(title='Absolute changes in USD', range=range),
                      yaxis2=dict(title='BTC in USD (in gold)',
                                  range=[df['btc_usd'].min(), df['btc_usd'].max()],
                                  overlaying='y', side='right'))

    fig.show()

def plotOptionPricesChangedPercent(df, strikes):

    fig = go.Figure()

    for i, strike in enumerate(strikes):
        fig.add_trace(go.Scatter(x=df['timestamp'],
                                 y=df[f'option_{strike}_changed_percent'],
                                 name=f'% change option {strike}', yaxis='y',
                                 line=dict(color=colors[i % len(colors)])))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_usd_changed_percent'],
                             name='% change BTC', yaxis='y',
                             line=dict(color='black')))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_usd'],
                             name='BTC price in USD on separate axis', yaxis='y2',
                             line=dict(color='gold')))
    '''
    '''
    range = [min([df[f'option_{strike}_changed_percent'].min() for strike in strikes] + [df['btc_usd_changed_percent'].min()]),
             max([df[f'option_{strike}_changed_percent'].max() for strike in strikes] + [df['btc_usd_changed_percent'].max()])]

    fig.update_layout(width=1600, height=800)
    fig.update_layout(title="Changes in % vs BTC price",
                      yaxis=dict(title='Changes in %', range=range),
                      yaxis2=dict(title='BTC in USD (in gold)',
                                  range=[df['btc_usd'].min(), df['btc_usd'].max()],
                                  overlaying='y', side='right')
                      )

    fig.show()

def plotOptionPricesChangedPercentAll(df, strikes):

    fig = go.Figure()

    for i, strike in enumerate(strikes):
        fig.add_trace(go.Scatter(x=df['timestamp'],
                                 y=df[f'option_{strike}_percent_all'],
                                 name=f'% change {strike} option', yaxis='y',
                                 line=dict(color=colors[i % len(colors)])))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_percent_all'],
                             name='% change BTC', yaxis='y',
                             line=dict(color='black')))

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['btc_usd'],
                             name='BTC price in USD on separate axis', yaxis='y2',
                             line=dict(color='gold')))
    '''
    '''
    range = [min([df[f'option_{strike}_percent_all'].min() for strike in strikes] + [df['btc_percent_all'].min()]),
             max([df[f'option_{strike}_percent_all'].max() for strike in strikes] + [df['btc_percent_all'].max()]) * 1.01]

    fig.update_layout(width=1600, height=800)
    fig.update_layout(title="Complete changes in % vs BTC price",
                      yaxis=dict(title='Complete changes in %', range=range),
                      yaxis2=dict(title='BTC in USD (in gold)',
                                  range=[df['btc_usd'].min(), df['btc_usd'].max() * 1.01],
                                  overlaying='y', side='right')
                      )

    fig.show()

def calcGains(df, strikes):
    dfNew = pd.DataFrame(df['timestamp'])
    dfNew = pd.concat([dfNew, df['btc_usd']], axis=1)

    dfNew.loc[:, 'btc_percent_all'] = (df['btc_usd'] - df.iloc[-1]['btc_usd']) / (df.iloc[-1]['btc_usd'] / 100)

    for i, strike_price in enumerate(strikes):
        option_usd_col_name = f'option_{strike_price}_usd'
        dfNew[option_usd_col_name] = df[option_usd_col_name].copy()
        dfNew[f'option_{strike_price}_percent_all'] = (
                                                              df[option_usd_col_name]
                                                              -
                                                              df.loc[df[option_usd_col_name].last_valid_index(), option_usd_col_name]
                                                      ) / (
                                                              df.loc[df[option_usd_col_name].last_valid_index(), option_usd_col_name]
                                                              /
                                                              100
                                                      )
    return dfNew

def plotSurface(df):
    fig = go.Figure(data=[go.Surface(
        z=df.iloc[:, 2:].fillna(0).values,
        x=df.iloc[:, 2:].columns,
        y=df['timestamp'],
        colorscale='RdBu'
    )])

    fig.update_layout(title='Option Prices over time by strike',
                      scene=dict(
                          xaxis=dict(title='Strike'),
                          yaxis=dict(title='Time'),
                          zaxis=dict(title='Price')
                      ),
                      width=1300, height=1200
                      )

    fig.show()
