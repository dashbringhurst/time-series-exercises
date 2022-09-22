import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import acquire
import requests

def prep__sales_data():
    '''This function takes in the saved csv file for sales data and saves it to a variable as a dataframe. The extra
    index column is dropped and the sale_date is converted to datetime format. The new sale_date is set as the index
    and sorted. A new column month is added with the month name for each observation. A day column is created with
    the day name for each observation. A sales_total column is created with the calculated total sales price for each
    observation, calculated by multiplying the item_price by the sale_amount. The function returns the prepared
    dataframe.'''
    # save the sales data csv to a variable
    df = pd.read_csv('store_item_sales.csv')
    # drop the extra index column
    df = df.drop(columns='Unnamed: 0')
    # remove the time section of the string in sale_date
    df.sale_date = df.sale_date.str.replace(' 00:00:00 GMT', '')
    # convert sale_date to datetime format
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y')
    # set sale_date as the index and sort
    df = df.set_index('sale_date').sort_index()
    # create a new column called month that contains the month name for each observation
    df['month'] = df.index.month_name()
    # create a new column called day that contains the day name for each observation
    df['day'] = df.index.day_name()
    # create a new column called sales_total that contains the item_price multiplied by the sale_amount
    df['sales_total'] = df.item_price * df.sale_amount
    # return the prepared dataframe
    return df

def prep_ops():
    '''This function pulls the opsd_germany csv from an html address and saves it to a variable as a dataframe.
    The dataframe is cleaned by making column names python-friendly and setting and sorting the date as the index.
    Three new columns are added: non_renew, month and year. The values for wind and solar are added together and 
    saved to the wind_solar column. The solar column nulls are filled with 0 first since the values started later
    in time, indicating that solar energy was available after wind energy. Wind energy nulls are filled with 0 and
    the two columns are added again and saved to wind_solar. This effectively handles all null values. The function
    returns the prepared dataframe.'''
    # pull the csv from the website and save to a variable
    ops = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    # covert column names to all lower case and replace the + symbol with _
    ops.columns = ops.columns.str.lower().str.replace('+', '_')
    # convert the date column to datetime format
    ops.date = pd.to_datetime(ops.date)
    # set the date column as the index and sort
    ops = ops.set_index('date').sort_index()
    # add a column for the month with the month name of each observation (string)
    ops['month'] = ops.index.month_name()
    # add a column for the year with the year of each observation (int)
    ops['year'] = ops.index.year
    # add the wind and solar columns and save the values to wind_solar
    ops['wind_solar'] = ops.wind + ops.solar
    # add a column for non-renewable consumption, calculated by subtracting wind_solar from consumption
    ops['non_renew'] = ops.consumption - ops['wind_solar']
    # fill the null values in the solar column with 0
    ops.solar = ops.solar.fillna(0)
    # add the wind_solar values again now that solar nulls have been filled
    ops['wind_solar'] = ops.wind + ops.solar
    # fill the null values in the wind column with 0
    ops.wind = ops.wind.fillna(0)
    # add the wind_solar values again; this should remove any remaining nulls
    ops['wind_solar'] = ops.wind + ops.solar
    # calculate the non-renewable consumption again and save to a variable
    ops.non_renew = ops.consumption - ops.wind_solar
    # return the prepared dataframe
    return ops