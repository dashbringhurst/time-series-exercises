import pandas as pd
import numpy as np
import requests

def get_items(base_url, endpoint):
    '''This function takes in two arguments, a base url and an endpoint url, and retrieves items data using requests.get
    and .json(). The function iterates through pages and pulls the data from each page until next_page is a NoneType. 
    The function returns a dataframe of the data from all pages.'''
    items = []
    while True:
        url = base_url + endpoint
        response = requests.get(url)
        data = response.json()
        items.extend(data['payload']['items'])
        endpoint = data['payload']['next_page']
        if endpoint is None:
            break
    return pd.DataFrame(items)

def get_stores(base_url, endpoint):
    '''This function takes in two arguments, a base url and an endpoint url, and retrieves stores data using requests.get
    and .json(). The function iterates through pages and pulls the data from each page until next_page is a NoneType. 
    The function returns a dataframe of the data from all pages.'''
    stores = []
    while True:
        url = base_url + endpoint
        response = requests.get(url)
        data = response.json()
        stores.extend(data['payload']['stores'])
        endpoint = data['payload']['next_page']
        if endpoint is None:
            break
    return pd.DataFrame(stores)

def get_sales(base_url, endpoint):
    '''This function takes in two arguments, a base url and an endpoint url, and retrieves sales data using requests.get
    and .json(). The function iterates through pages and pulls the data from each page until next_page is a NoneType. 
    The function returns a dataframe of the data from all pages.'''
    sales = []
    while True:
        url = base_url + endpoint
        response = requests.get(url)
        data = response.json()
        sales.extend(data['payload']['sales'])
        endpoint = data['payload']['next_page']
        if endpoint is None:
            break
    return pd.DataFrame(sales)

def get_data(base_url, pages, loc):
    '''This function takes in three arguments:
            - base url for the data
            - number of pages expressed as range(x1,x2)
            - location of items expressed as a string
        and collects data from url pages using requests.get and .json().
        The function returns a dataframe of the acquired data for the given range of pages.'''
    items = []
    for page_no in pages:
        endpoint = str(page_no)
        response = requests.get(base_url+endpoint).json()['payload'][loc]
        items.extend(response)
    return pd.DataFrame(items)

def concat_sales_data(sales_df, items_df, store_df):
    df = sales_df.rename(columns={'item': 'item_id', 'store': 'store_id'})
    df = pd.merge(sales_df, items_df, how='left', on='item_id')
    df = pd.merge(df, store_df, how='left', on='store_id')
    return df

