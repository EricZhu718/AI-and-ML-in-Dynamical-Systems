#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from asyncio.windows_events import NULL
import os
import sys
from tokenize import String
from xml.etree.ElementTree import tostring

sys.path.append('MLInStocks/analysis')

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback_context  # pip install dash (version 2.0.0 or higher)

import import_data
import singular_spectrum_analysis as SSA

unprocessed_df = NULL
SSA_df = NULL

app = Dash(__name__, external_stylesheets=['/assets/styles.css'])

app.layout = html.Div([
    html.H1("Stock Data", id = 'Stock-Data-Header', style = {'width' :'50%', 'margin': 'auto', 'text-align': 'center'}),
    
    html.Div(id = 'inputs', children = [
        dcc.Input(
            id = 'Ticker',
            placeholder='Enter a Ticker (S&P 500 Default)',
            type='text',
            value='^GSPC'
        ),

        html.Button('Run SSA', id = 'SSA', n_clicks=0)
    ]),
    
    dcc.Graph(
        id = 'Graph'
    )
])

data_type = 'unprocessed'
unprocessed_df = import_data.getDataFrame('2018-01-01', '2022-01-01') 

# callback for the text input field
@app.callback(
    Output("Graph", "figure"),
    Input("Ticker", 'value'),    
    Input("SSA", 'n_clicks')
)
def update_output(input1, input2):
    global unprocessed_df
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    fig = {
        'data': [{
            'x': NULL,
            'y': NULL,
            'type': 'line',
            'color': 'black'
        }],
        'layout': {
            # You need to supply the axes ranges for smooth animations
            'xaxis': {
                'range': [unprocessed_df['Date'][0], unprocessed_df['Date'][len(unprocessed_df['Date'])-1]]
            },
            'yaxis': {
                'range': [800, 5000]
            },

            'transition': {
                'duration': 2000,
                'easing': 'cubic-in-out'
            }
        }
    }
    if 'SSA.n_clicks' in changed_id:
        global data_type
        SSA_df = SSA.get_SSA(unprocessed_df['Open'])
        # print(graph_df)
        print("SSA finished")
        fig['data'][0]['x'] = unprocessed_df['Date']
        fig['data'][0]['y'] = SSA_df

        fig['data'].append({
            'x': unprocessed_df['Date'],
            'y': unprocessed_df['Open'],
            'type': 'line',
            'color': 'blue'
        })

    elif 'Ticker.value' in changed_id:
        print('1: '+ input1.upper())
        
        fig['data'][0]['x'] = unprocessed_df['Date']
        fig['data'][0]['y'] = unprocessed_df['Open']
    else: 
        global data_type
        SSA_df = SSA.get_SSA(unprocessed_df['Open'])
        # print(SSA_df)
        graph_df = []
        for index in range(len(SSA_df)):
            graph_df.append({'Date': unprocessed_df['Date'][index], 'SSA': SSA_df[index]})
        # print(graph_df)
        fig['data'][0]['x'] = unprocessed_df['Date']
        fig['data'][0]['y'] = unprocessed_df['Open']
    return fig





app.run_server(debug=True)

