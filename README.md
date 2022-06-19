

[![Generic badge](https://img.shields.io/badge/Python-3.8-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Dash-2.0-blue.svg)](https://shields.io/)
![Heroku](https://github.com/DenisOH/pyheroku-badge/blob/master/img/deployed.svg)
# Stock-Forecast-Dash
Project guide and refernce credit: [Crio.do](https://www.crio.do/projects/python-forecasting-stocks-dash/)


Stock Price Forecast App is based on Machine Learning. By providing number of days 
, we can predict trend in Stock Price. The frontend of App is based on Dash-plotly
framework. Model is predicting stock price  using Support Vector Regression
algorithm. App can predict next 5-10 days trend using past 60 days data.

check this App on heroku: [stock-predict-dash.herokuapp.com](https://stock-predict-dash.herokuapp.com/)

## Screenshots
<img src="https://user-images.githubusercontent.com/89059809/174493701-b5485e58-ecae-4a4e-8706-4402fc800395.png" width="750" height="400" alt='Screenshot1'>
<img src="https://user-images.githubusercontent.com/89059809/174493703-fd137ce4-e152-4f6e-b33d-93276e9000eb.png" width="750" height="400" alt='Screenshot2'>


## Getting Started

* Enter **Stock_ticker** Eg. _AAPL_ is for Apple. hit `Submit` button.
* You can Specify Time range, default is 1st Jan 2020 till today.
* Click on `Stock Price` button to see stock's actual price trend
* Click `Indicators` button to see EMA20 Indicator on Stock price trend graph
* Enter number between 1-15 and hit `Forecast` button, it will take some time to load predicted future trend 
 
## Download
 
```bash
  git clone https://github.com/Niraj-kumbhar/Stock_Forcast_project.git
```
    
## Requirements
* python3.x
* dash
* Flask
* lxml
* numpy
* pandas
* plotly
* scikit-learn
* gunicorn
* scipy
* sklearn
* yfinance


Install libraries from _requirements.txt_ file
```
pip install -r requirements.txt
```

## Documentation

* [Dash-Plotly](https://dash.plotly.com/) - Framework for interactive web applications
* [yfinance](https://pypi.org/project/yfinance/) - offers a threaded and Pythonic way to download market data from [Yahoo!Ⓡ finance](https://finance.yahoo.com/).


## Contributors
[Manisha Ahlawat](https://github.com/ahlawat-manisha)


## Disclaimer

This software is for educational purposes only. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS. Do not risk money which you are afraid to lose. There might be bugs in the code - this software DOES NOT come with ANY warranty.

