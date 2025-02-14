import pandas as pd
import numpy as np


def data_load(path, format):
    if format == 'csv':
        data = pd.read_csv(path)
    elif format == 'xlsx':
        data = pd.read_excel(path)
    return data

def df_load(df,x_column,y_column, ctx):
    df[x_column] = df[x_column].astype(str)
    df[x_column] = pd.to_datetime(df[x_column], utc=True)
    df = df.set_index(x_column)
    default_interval = df.index.inferred_freq
    if default_interval == None:
        df = df.groupby(df.index).mean()
        df = df.asfreq(ctx['interval'])
        df = df.resample(ctx['interval']).mean()
    df[y_column] = df[y_column].replace('',np.nan).astype(float)
    df[y_column] = df[y_column].interpolate()
    df[y_column] = df[y_column].bfill()

    
    return df
