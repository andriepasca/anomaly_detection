import streamlit as st
from func.data_loader import data_load, df_load
from func.anomaly_detector import seasonal_anomaly, _join_df_with_anomaly, isolation_forest
from func.visualizer import plot_base_line, plot_anomalies

st.title('Anomaly Detection on Energy Dataset')
st.write('This is an experimental project for anomaly detection using energy consumption and generation dataset. Two anomaly detection methods (adtk and isolation forest) were used in this project.')
st.write('The dataset source: https://data.open-power-system-data.org/time_series/')

st.subheader('Data Preview')

# url = './sample_data/time_series_60min_singleindex.csv'
url = 'https://data.open-power-system-data.org/time_series/2020-10-06/time_series_15min_singleindex.csv'
with st.status("Downloading data...", expanded=True) as status:
    data = data_load(url)
    st.dataframe(data)
    status.update(
        label="Download complete!", state="complete", expanded=True
    )

col1, col2 = st.columns(2)
columns = tuple(list(data))
columns_val = columns[2::]
x_column = columns[0]
y_column = col1.selectbox(
    "select a column for anomaly detection ",
    columns_val,
)
df = df_load(data,x_column,y_column)
unique_years = ['All']
unique_years.extend(list(df.index.year.unique()))
year = col2.selectbox(
    "select a column for years ",
    unique_years,
)
st.write("You selected column :", y_column, '. Years : ', year)
if year != 'All':
    df = df[df.index.year == year]

st.subheader('Selected DataFrame')
st.dataframe(df[y_column], use_container_width=True)

st.subheader('Base Plot')
with st.status("Generating graph...", expanded=True) as status:
    base_plot = plot_base_line(df, y_column)
    st.write(base_plot)
    status.update(
        label="Graph complete!", state="complete", expanded=True
    )

st.subheader('Seasonal Anomaly')
with st.status("Generating graph...", expanded=True) as status:
    seasonal_anomalies = seasonal_anomaly(df[y_column])
    df_level_anomalies = _join_df_with_anomaly(df, seasonal_anomalies, anomaly_type='seasonal')
    seasonal_anomalies_plot = plot_anomalies(df_level_anomalies, y_column, anomaly_type='seasonal')
    st.write(seasonal_anomalies_plot)
    status.update(
        label="Graph complete!", state="complete", expanded=True
    )

st.subheader('Isolation Forest Anomaly')
with st.status("Generating graph...", expanded=True) as status:
    isolation_anomalies = isolation_forest(df[[y_column]])
    df_isolation_anomalies = _join_df_with_anomaly(df, isolation_anomalies, anomaly_type='isolationforest')
    isolation_anomalies_plot = plot_anomalies(df_isolation_anomalies, y_column, anomaly_type='isolationforest')
    st.write(isolation_anomalies_plot)
    status.update(
        label="Graph complete!", state="complete", expanded=True
    )
