#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from xml.etree.ElementTree import tostring

sys.path.append('MLInStocks/analysis')

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback_context  # pip install dash (version 2.0.0 or higher)

import import_data

app = Dash(__name__, external_stylesheets=['/assets/styles.css'])

unprocessed_df = import_data.getDataFrame('1985-01-01', '2021-01-01')

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


# callback for the text input field
@app.callback(
    Output("Graph", "figure"),
    Input("Ticker", 'value'),    
    Input("SSA", 'n_clicks')
)
def update_output(input1, input2):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    print(changed_id)
    print('1: '+ input1)
    print('2: '+ str(input2))
    fig = px.line(unprocessed_df, 
        x="Date", y="Open")
    return fig



app.run_server(debug=True)

