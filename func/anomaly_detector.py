import pandas as pd
from adtk.data import validate_series
from adtk.detector import SeasonalAD
from sklearn.ensemble import IsolationForest
import warnings
warnings.simplefilter(action="ignore", category=UserWarning)


def seasonal_anomaly(series,config={'c':1,'side':'both','window':3}):
    s = validate_series(series)
    model = SeasonalAD(c=config['c'], side=config['side'])
    anomalies = model.fit_detect(s)
    return anomalies

def _join_df_with_anomaly(df, anomalies, config):
    anomalies = pd.DataFrame(anomalies)
    anomalies.fillna(False, inplace=True)
    anomalies.reset_index(drop=True)
    
    anomaly_column = config['anomaly_column']
    df[anomaly_column]=anomalies.to_numpy()
    return df

def isolation_forest(df):
    df_without_index = df.reset_index(drop=True)
    model = IsolationForest(bootstrap=True,contamination=0.1, max_samples=0.2)
    model.fit(df_without_index)
    anomalies = pd.Series(model.predict(df_without_index)).apply(lambda x: True if (x == -1) else False)
    return anomalies
