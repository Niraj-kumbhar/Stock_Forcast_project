def predictionModel(n_days, stock_code):
    '''
    This function will get called by callbacks.
    It will create ML model to predict stock price based on provided number of days and stock ticker
    '''

    # importing libraries 
    import yfinance as yf
    import plotly.graph_objects as go
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.svm import SVR
    from datetime import date, timedelta

    df = yf.download(stock_code, period='60d') # downloading data for 60days
    df.reset_index(inplace=True)
    df['Days'] = df.index # adding new column in dataset

    days = []
    for i in range(len(df['Days'])):
        days.append([i])
    
    # Splitting the dataset
    X = days
    y = df.Close

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

    # We are going to use GridSearchCV method
    # for getting best parameters for our model
    # first we will provide some parameters as Dict here
    paramters = {
        'C':[0.001,0.01,0.1,1,100,1000],
        'epsilon': [
                    0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10,
                    50, 100, 150, 1000
                ],
        'gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5, 8, 40, 100, 1000]
    }

    # we will use Support Vector Regressor and kernel as Radial Basis Function
    gsc = GridSearchCV(
        estimator=SVR(kernel='rbf'),
        param_grid=paramters,
        cv=10,
        scoring='neg_mean_absolute_error'
    )

    grid_result = gsc.fit(X_train,y_train)

    # storing and using best parameters
    # best parameters = min error
    best_param = grid_result.best_params_
    svr_model = SVR(kernel='rbf', C=best_param['C'], epsilon=best_param['epsilon'], gamma=best_param['gamma'])
    svr_model.fit(X_train, y_train)

    output_days = []
    for i in range(1,n_days+1): # adding n days provided by user to our 60 day
        output_days.append([i+X_test[-1][0]]) # 60 + n

    dates = []
    current = date.today()
    for i in range(n_days): # creating timeline for future dates
        current += timedelta(days=1)
        dates.append(current)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
                x=dates, 
                y=svr_model.predict(output_days),
                mode='lines+markers',
                name='data'))
    fig.update_layout(
        title="Predicted Close Price of next " + str(n_days - 1) + " days",
        xaxis_title="Date",
        yaxis_title="Closed Price"
    )

    return fig