import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import prepare
from datetime import datetime
from sklearn.metrics import mean_squared_error
from math import sqrt
from pandas.plotting import register_matplotlib_converters
import statsmodels.api as sm
from statsmodels.tsa.api import Holt

def prep_data():
    df = pd.read_csv('landtemp_state.csv')
    df = df.dropna()
    df.columns = df.columns.str.lower()
    df = df.rename(columns={'averagetemperature':'avg_temp', 'averagetemperatureuncertainty':'avg_temp_uncertain'})
    df.avg_temp = (df.avg_temp * 1.8) + 32
    df.dt = pd.to_datetime(df.dt)
    df = df.set_index('dt').sort_index()
    df_us = df[df.country=='United States']
    df = df_us[df_us.state=='Texas']
    df = df.avg_temp.resample('m').mean()
    df = pd.DataFrame(df)
    df = (df['1820':'2012'])
    return df

def split_data(df):
    train_size = int(len(df) * 0.5)
    validate_size = int(len(df) * 0.3)
    test_size = int(len(df) - train_size - validate_size)
    validate_end_index = train_size + validate_size
    train = df[:train_size]
    validate = df[train_size:validate_end_index]
    test = df[validate_end_index:]
    train = pd.DataFrame(train)
    validate = pd.DataFrame(validate)
    test = pd.DataFrame(test)
    return train, validate, test

def plot_data(df, train, validate, test):
    for col in df.columns:
        plt.figure(figsize=(14,8))
        plt.plot(train[col])
        plt.plot(validate[col])
        plt.plot(test[col])
        plt.ylabel('Temperature (Fahrenheit)')
        plt.title('Average Temperature in Texas over Time')
        plt.show()

def evaluate(target_var, validate, yhat_df):
    '''
    This function will take the actual values of the target_var from validate, 
    and the predicted values stored in yhat_df, 
    and compute the rmse, rounding to 0 decimal places. 
    it will return the rmse. 
    '''
    rmse = round(mean_squared_error(validate[target_var], yhat_df[target_var], squared=False), 0)
    return rmse

def plot_and_eval(target_var, train, validate, yhat_df):
    '''
    This function takes in the target var name (string), and returns a plot
    of the values of train for that variable, validate, and the predicted values from yhat_df. 
    it will als lable the rmse. 
    '''
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label='Train', linewidth=1)
    plt.plot(validate[target_var], label='Validate', linewidth=1)
    plt.plot(yhat_df[target_var], label='prediction')
    plt.ylabel('Temperature (Fahrenheit)')
    plt.title('Average Temperature in Texas over Time')
    rmse = round(mean_squared_error(validate[target_var], yhat_df[target_var], squared=False), 0)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.legend()
    plt.show()

# create an empty dataframe
eval_df = pd.DataFrame(
    columns=['model_type', 'target_var', 'rmse'])
eval_df

# function to store the rmse so that we can compare
def append_eval_df(model_type, target_var, validate, yhat_df):
    '''
    this function takes in as arguments the type of model run, and the name of the target variable. 
    It returns the eval_df with the rmse appended to it for that model and target_var. 
    '''
    rmse = round(mean_squared_error(validate[target_var], yhat_df[target_var], squared=False), 0)
    d = {'model_type': [model_type], 'target_var': [target_var],
        'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)





