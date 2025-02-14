import streamlit as st
from func.data_loader import data_load, df_load
from func.anomaly_detector import seasonal_anomaly, _join_df_with_anomaly, isolation_forest
from func.visualizer import plot_base_line, plot_anomalies

st.title('Anomaly Detection for Time Series Dataset')



# ----------------- Source Definition --------------------
context_dict = {
    'Wind turbine SCADA data' : {
        'text': 'This is the experimental project for anomaly detection using SCADA data in the context of wind farm.',
        'url' : 'https://data.mendeley.com/datasets/tm988rs48k/2',
        'path': './sample_data/VestasV52_10_min_raw_SCADA_DkIT 30_Jan2006-12_Mar2020.xlsx',
        'interval': '10T',
        'format': 'xlsx'
    },
    'Energy consumption' : {
        'text': 'This is an experimental project for anomaly detection using energy consumption and generation dataset. The dataset source can be found here: https://data.open-power-system-data.org/time_series/',
        'url' : 'https://data.open-power-system-data.org/time_series/2020-10-06/time_series_15min_singleindex.csv',
        'path': './sample_data/time_series_60min_singleindex.csv',
        'interval': 'H',
        'format': 'csv'
    },
}

context = st.selectbox(
    'Select the dataset',
    context_dict.keys()
)
ctx = context_dict[context]
st.write(ctx['text'])
st.write('Dataset URL', ctx['url'])

if st.button(label='Confirm', key='context_button'):
    path = ctx['path']
    format = ctx['format']

    # ----------------- Data Preview --------------------
    st.subheader('Data Preview')
    with st.status("Downloading data...", expanded=True) as status:
        data = data_load(path, format)
        status.update(
            label="Download complete!", state="complete", expanded=True
        )
    
    st.session_state['data'] = data


if 'data' in st.session_state:
    data = st.session_state['data']
    st.dataframe(data)
    # -----------------Filter--------------------
    columns = tuple(list(data))
    columns_idx = columns
    columns_val = columns
    x_column = columns[0]
    col1, col2 = st.columns(2)
    x_column = col1.selectbox(
        'select a column contains datetime',
        columns_idx, index=0
    )
    y_column = col2.selectbox(
        "select a column contains value ",
        columns_val, index=len(columns_val)-1
    )
    
    df = df_load(data,x_column,y_column, ctx)

    unique_years = ['All']
    unique_years.extend(list(df.index.year.unique()))
    start_year = col1.number_input('enter start year', min_value=unique_years[1], max_value=unique_years[-1], value=unique_years[1])
    end_year = col2.number_input('enter end year', min_value=unique_years[1], max_value=unique_years[-1], value=unique_years[-1])
    interval_dict = {
        'Hourly': 'H',
        'Daily' : 'D',
        'Weekly': 'W',
        'Monthly': 'M'
    }
    interval = col1.selectbox(
        "select frequency",
        interval_dict.keys(), index=len(interval_dict)-1
    )
    st.write("You selected column :", y_column, '. Year : ', start_year, ' to ', end_year, '. Interval : ', interval)

    if st.button(label='Confirm', key='dataframe_button'):
        df = df[(df.index.year >= start_year) & (df.index.year <= end_year)]
        df = df.resample(interval_dict[interval]).mean()

        # ----------------- Selected DataFrame--------------------
        st.subheader('Selected DataFrame')
        st.dataframe(df[y_column], use_container_width=True)



        # ----------------- Data Visualization--------------------
        ## --------------------- Base Plot------------------------
        st.subheader('Base Plot')
        with st.status("Generating graph...", expanded=True) as status:
            base_plot = plot_base_line(df, y_column)
            st.write(base_plot)
            status.update(
                label="Graph complete!", state="complete", expanded=True
            )

        ## ------------------- Isolation Forest ----------------------
        st.subheader('Machine Learning Based Detection - Isolation Forest')
        with st.status('Detecting Anomaly...', expanded=True) as status:
            isolation_anomalies = isolation_forest(df[[y_column]])
            config={
                'anomaly_column':'isolation_ad',
                'legend_name': 'isolation forest anomaly',
                'color':'rgba(222,40,41,0.8)'
            }
            df_isolation_anomalies = _join_df_with_anomaly(df, isolation_anomalies, config)
            status.update(
                label="Detection complete!", state="complete", expanded=True
            )
        with st.status("Generating graph...", expanded=True) as status:
            isolation_anomalies_plot = plot_anomalies(df_isolation_anomalies, y_column, config)
            st.write(isolation_anomalies_plot)
            status.update(
                label="Graph complete!", state="complete", expanded=True
            )

        # ## ---------------------- Seasonal ------------------------
        # st.subheader('Statistical Analysis Based Detection')
        # with st.status('Detecting Anomaly...', expanded=True) as status:
        #     seasonal_anomalies = seasonal_anomaly(df[y_column])
        #     config={
        #         'anomaly_column':'seasonal_ad',
        #         'legend_name': 'seasonal anomaly',
        #         'color':'rgba(249,123,34,0.8)'
        #     }
        #     df_seasonal_anomalies = _join_df_with_anomaly(df, seasonal_anomalies, config)
        #     status.update(
        #         label="Detection complete!", state="complete", expanded=True
        #     )
        # with st.status("Generating graph...", expanded=True) as status:
        #     seasonal_anomalies_plot = plot_anomalies(df_seasonal_anomalies, y_column, config)
        #     st.write(seasonal_anomalies_plot)
        #     status.update(
        #         label="Graph complete!", state="complete", expanded=True
        #     )
