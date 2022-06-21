#first import all of this lib
import dash
from dash import dcc
from dash import html
from datetime import date, datetime as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#from matplotlib.pyplot import title
import yfinance as yf
import pandas as pd
#import plotly.graph_objs
#import plotly.graph_objects as go
import plotly.express as px
#import pandas_datareader.data as web
from model import predictionModel

app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(
    [  
        html.Div(
            [
                html.H2("Welcome to the Stock Trend Prediction App!", className="heading"),
                html.Div(
                    [
                    # Input box for to enter stock ticker, default value will be 'SBIN.NS'
                    dcc.Input(id='stock_code', value= '',placeholder= 'Input Stock Ticker here', type= 'text', className='inputs'),
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
                            # end_date = dt.now(),
                            start_date = date(2020,1,1),
                            className='inputs'
                        )
                    ],className=''

                ),

                html.Div(
                    [
                        #two buttons below
                        html.Button('Stock Price', id='stock_price', className='buttons'),
                        html.Button('Indicators', id='indicators', n_clicks=0, className='buttons'),
                        
                    ],className=''
                ),
                html.Div(
                    [
                        # Input box to enter number of days to forecast future price and button to initiate task
                        dcc.Input(id='n_days',value = '', type='text', placeholder='Number of Days for forecast', className='inputs'),
                        html.Button('Forecast', id='Forecast', className='buttons', n_clicks=0)
                    ],className=''
                )
            
            ],className='nav'
        ),

        # 2nd part, this should be on right side of screen, will display graph

        html.Div(
            [
            dcc.Loading( id='loading1', color='#3b3b3b',children=[html.Div(
                [
                    html.Img(id='logo', className='imglogo'),
                    html.H2(id='ticker')
                ],className='header'
            ),
            html.Div(id='description', className='info')], type='circle'),
            dcc.Loading(children=[html.Div([], id='stonks-graph', className='graphs')], id='loading2', type='graph'),
            dcc.Loading(id='loading3',
                children=[html.Div([], id='forecast-graph', className='graphs')],
                type='graph')


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
    desc = """
    Hey! Enter stock Ticker to get information

        1. Enter Stock ticker at input(AAPL for Apple.inc)
        2. Hit Submit button and wait
        3. Click Stock price button and Indicator button to get trend of stock price
        4. Enter number of days between 1-15 to forecast the trend and hit forecast button
        5. wait.....and Hurreeyy !! you got it."""
    if n==0 or stock_code=='' :
        return 'https://www.linkpicture.com/q/stonks.jpg','',desc
    else:
        tk = yf.Ticker(stock_code)
        sinfo = tk.info
        #df = pd.DataFrame(sinfo)
        return sinfo['logo_url'], sinfo['shortName'], sinfo['longBusinessSummary']


    
    
#callback for updating graph for selected time range
@app.callback(
    Output(component_id='stonks-graph', component_property='children'),
    [Input(component_id='stock_price', component_property='n_clicks'),
    Input('indicators', 'n_clicks'),
    Input('date-range','start_date'),
    Input('date-range','end_date')],
    [State(component_id='stock_code', component_property='value')]
)
def update_mygraph(n, ind, start, end,stock_code):
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

        #stock code will match on yahoo finance and data will fetch to generate graph
        df = pd.DataFrame(yf.download(stock_code,start=start, end=end))
        df.reset_index(inplace=True)
        df['Date']=pd.to_datetime(df['Date'])
        df['ema20'] = df['Close'].rolling(20).mean()
        fig = px.line(
             df,
             x='Date',
             y=['Close'],
             title='Stock Trend'
         )
        fig.update_traces(line_color='#ef3d3d')
        #go.Figure(data=[
        #         go.Candlestick(
        #             x=df['Date'],
        #             open=df['Open'], high=df['High'],
        #             low=df['Low'], close=df['Close']
        #         ),
                #go.Scatter()
        #    ])
        
        if ind in [1,3,5,7,9,11,13,15,17]:
            fig.add_scatter(x=df['Date'], y=df['ema20'], line=dict(color= 'blue', width=1), name='EMA20')
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            xaxis_title="Date",
            yaxis_title="Closed Price")
        
        return dcc.Graph(figure=fig)

@app.callback(
    Output(component_id='forecast-graph', component_property='children'), 
    [Input(component_id='Forecast', component_property='n_clicks'),
    Input(component_id='n_days', component_property='value')],
    [State(component_id='stock_code', component_property='value')]
)
def forecast(n, n_days, stock_code):
    if n == None:
        return ['']
    if stock_code == '':
        raise PreventUpdate
    fig = predictionModel(int(n_days)+1, stock_code)
    return dcc.Graph(figure=fig)
    


if __name__ =='__main__':
    app.run_server(debug = True)