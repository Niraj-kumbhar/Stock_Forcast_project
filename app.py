#first import all of this lib
import dash
from dash import dcc
from dash import html
from datetime import date, datetime as dt
from dash.dependencies import Input, Output, State
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import pandas_datareader.data as web

app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(
    [  
        html.Div(
            [
                html.H2("Welcome to the Stock Dash App!", className=""),
                html.Div(
                    [
                    # Input box for to enter stock ticker, default value will be 'SBIN.NS'
                    dcc.Input(id='stock_code', value= 'SBIN.NS',placeholder= 'Input here', type= 'text', className='inputs'),
                    #html.Button('Submit', id='submit-stock', className='inputs', n_clicks=0)

                    ],className=''
                ),

                html.Div(
                    [
                        #Date range input, if nothing given default will be 1st jan 2020 to today
                        dcc.DatePickerRange(
                            id = 'date-range',
                            className='inputs'
                        )
                    ],className=''

                ),

                html.Div(
                    [
                        #two buttons below
                        html.Button('Stock Price', id='stock_price', className=''),
                        html.Button('Indicators', id='indicators', className=''),
                        # Input box to enter number of days to forcast future price and button to intiate task
                        dcc.Input(id='n_days',value = '', type='text', placeholder='Days here', className=''),
                        html.Button('Forecast', id='Forecast', className='')
                    ],className=''
                )
            
            ],className='nav'
        ),

        #2nd part, this should be on right side of screen, will display graph
        html.Div(
            [
            html.Div(
                [
                    html.Img(id='logo'),
                    html.P(id='ticker')
                ],className=''
            ),
            html.Div(id='description'),
            html.Div([], id='stonks'),
            #html.Div()


            ],className=''
        )
    ], className='container')



    
    

@app.callback(
    Output(component_id='stonks', component_property='children'),
    #Input(component_id='submit', component_property='n_clicks'),
    [Input(component_id='stock_code', component_property='value')],
    Input('date-range','start_date'),
    Input('date-range','end_date')
)
def update_mygraph(stock_code, start, end):
    
    #if start is not selected, we will assume it as 1st Jan 2020
    if start is None:
        start = date(2020, 1, 1)
    #if end date is not selected, set end date as current day
    if end is None:
        end = dt.today()

    #stock code will match on yahoo finance and data will fetch to genrate graph
    tk = yf.Ticker(stock_code)
    data = pd.DataFrame(tk.history(start=start, end=end))
    name = tk.info['shortName']
    fig = {'data': [{'x': data.index,'y': data.Close, 'type': 'Candlestick', 'name': stock_code}, ], 'layout': {'title': name}}
    return dcc.Graph(figure= fig)

if __name__ =='__main__':
    app.run_server(debug = True)