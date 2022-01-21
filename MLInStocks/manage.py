#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from asyncio.windows_events import NULL
import os
import sys
from tokenize import String
from xml.etree.ElementTree import tostring

from pyparsing import line

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
    
    
    fig = NULL
    data = NULL
    frames = NULL
    layout = NULL

    date_df = unprocessed_df['Date']

    if 'SSA.n_clicks' in changed_id:
        # SSA Button clicked
        SSA_df = SSA.get_SSA(unprocessed_df['Open'])

        open_df = unprocessed_df['Open']
        trace1 = go.Scatter(
            x = date_df[:2],
            y= open_df[:2],
            mode='lines',
            line = {'width': 1.5}
        )

        trace2 = go.Scatter(
            x = date_df[:2],
            y= SSA_df[:2],
            mode='lines',
            line = {'width': 1.5}
        )

        frames = [dict(data= [dict(type='scatter',
                           x=date_df[:k+1],
                           y=open_df[:k+1]),
                      dict(type='scatter',
                           x=date_df[:k+1],
                           y=SSA_df[:k+1])
                     ],
               traces= [0, 1],  
              )for k  in  range(1, len(date_df)-1)]

        layout = go.Layout(
            width=700,
            height=600,
            showlegend=False,
            hovermode='x unified',
            updatemenus=[
                dict(
                    type='buttons', showactive=False,
                    y=1.05,
                    x=1.15,
                    xanchor='right',
                    yanchor='top',
                    pad=dict(t=0, r=10),
                    buttons=[dict(label='Play',
                        method='animate',
                        args=[None, 
                            dict(
                                frame=dict(duration=1, 
                                redraw=False),
                                transition=dict(duration=0),
                                fromcurrent=True,
                                mode='immediate'
                            )]
                    )]
                ),
                dict(
                    type = "buttons",
                    direction = "left",
                    buttons=list([
                        dict(
                            args=[{"yaxis.type": "linear"}],
                            label="LINEAR",
                            method="relayout"
                        ),
                        dict(
                            args=[{"yaxis.type": "log"}],
                            label="LOG",
                            method="relayout"
                        )
                    ]),
                ),
            ]              
        )

        fig = go.Figure(data=[trace1, trace2], frames=frames, layout=layout)

        print('ran ssa')
    else: 
        # start up
        # SSA Button clicked
        SSA_df = SSA.get_SSA(unprocessed_df['Open'])

        open_df = unprocessed_df['Open']
        trace1 = go.Scatter(
            x = date_df,
            y= open_df,
            mode='lines',
            line = {'width': 1.5}
        )

        fig = go.Figure(data=[trace1])
    return fig





app.run_server(debug=True)

