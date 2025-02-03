import pandas as pd
import numpy as np


def data_load(url):
    data = pd.read_csv(url)
    return data

def df_load(df,x_column,y_column):
    # 
    df[x_column] = df[x_column].astype(str)
    df[x_column] = pd.to_datetime(df[x_column], utc=True)
    df = df.set_index(x_column)
    # df.drop(columns=x_column,inplace=True)
    df[y_column] = df[y_column].replace('',np.nan).astype(float)
    df[y_column] = df[y_column].interpolate()
    df[y_column] = df[y_column].fillna(method="bfill")
    
    return df