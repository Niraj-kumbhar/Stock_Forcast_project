#first import all of this lib
import dash
from dash import dcc
from dash import html
from datetime import date, datetime as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import yfinance as yf
import pandas as pd
import plotly.graph_objs
import plotly.graph_objects as go
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
                    dcc.Input(id='stock_code', value= '',placeholder= 'Input here', type= 'text', className='inputs'),
                    html.Button('Submit', id='submit-stock', className='buttons', n_clicks=0)

                    ],className=''
                ),

                html.Div(
                    [
                        #Date range input, if nothing given default will be 1st jan 2020 to today
                        dcc.DatePickerRange(
                            id = 'date-range',
                            min_date_allowed=dt(1995,8,5),
                            max_date_allowed=dt.today(),
                            initial_visible_month=dt.now(),
                            className='inputs'
                        )
                    ],className=''

                ),

                html.Div(
                    [
                        #two buttons below
                        html.Button('Stock Price', id='stock_price', className='buttons'),
                        html.Button('Indicators', id='indicators', className='buttons'),
                        
                    ],className=''
                ),
                html.Div(
                    [
                        # Input box to enter number of days to forcast future price and button to intiate task
                        dcc.Input(id='n_days',value = '', type='text', placeholder='Days here', className='inputs'),
                        html.Button('Forecast', id='Forecast', className='buttons')
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
                    html.H2(id='ticker')
                ],className='header'
            ),
            html.Div(id='description',),
            html.Div([], id='stonks-graph', className='graphs'),
            #html.Div()


            ],className='outputContainer'
        )
    ], className='container')


#callback for updating logo and stock description
@app.callback([
    Output('logo', 'src'),
    Output('ticker', 'children'),
    Output('description', 'children')],
    [Input('submit-stock', 'n_clicks')],
    [State('stock_code', 'value')]
)

def update_data(n, stock_code):
    #if user provided nothing, then default output will following
    if n==0 :
        return 'https://www.linkpicture.com/q/stonks_1.jpg','stonks','Hey! Enter stock Ticker to get information'
    else:
        tk = yf.Ticker(stock_code)
        sinfo = tk.info
        #df = pd.DataFrame(sinfo)
        return sinfo['logo_url'], sinfo['shortName'], sinfo['longBusinessSummary']


    
    
#callback for updating graph for selected time range
@app.callback(
    Output(component_id='stonks-graph', component_property='children'),
    [Input(component_id='stock_price', component_property='n_clicks'),
    Input('date-range','start_date'),
    Input('date-range','end_date')],
    [State(component_id='stock_code', component_property='value')]
)
def update_mygraph(n, start, end,stock_code):
    if n==0:
        return ''

    elif stock_code=='':
        raise PreventUpdate

    else:
        #if start is not selected, we will assume it as 1st Jan 2020
        if start is None:
            start = date(2020, 1, 1)
        #if end date is not selected, set end date as current day
        if end is None:
            end = dt.today()

        #stock code will match on yahoo finance and data will fetch to genrate graph
        tk = yf.Ticker(stock_code)
        name = tk.info['shortName']
        df = pd.DataFrame(yf.download(stock_code,start=start, end=end))
        df.reset_index(inplace=True)
        df['Date']=pd.to_datetime(df['Date'])
        fig = go.Figure(data=[
                go.Candlestick(
                    x=df['Date'],
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close']
                )
            ])
        fig.update_layout(xaxis_rangeslider_visible=False)
        return dcc.Graph(figure=fig)



if __name__ =='__main__':
    app.run_server(debug = True)