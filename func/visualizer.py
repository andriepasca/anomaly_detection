import plotly.graph_objects as go


def plot_base_line(df,y_column):
    figure = go.Figure()
    figure.add_trace(go.Scatter(name=y_column, x = df.index, y=df[y_column], marker=dict(color='rgba(50,50,50,0.3)')))
    return figure

def plot_anomalies(df, y_column, anomaly_type):
    figure = go.Figure()
    if anomaly_type == 'seasonal':
        config={
            'anomaly_column':'seasonal_ad',
            'legend_name': 'seasonal anomaly',
            'color':'rgba(249,123,34,0.8)'
        }
    elif anomaly_type == 'isolationforest':
        config={
            'anomaly_column':'isolation_ad',
            'legend_name': 'collective anomaly',
            'color':'rgba(255,217,61,0.8)'
        }
    # plot baseline
    figure.add_trace(go.Scatter(name=y_column, x = df.index, y=df[y_column], marker=dict(color='rgba(50,50,50,0.3)')))

    # plot anomaly points
    anomaly_df = df
    anomaly_df = anomaly_df[anomaly_df[config['anomaly_column']]==True]

    figure.add_trace(go.Scatter(name=config['legend_name'], x = anomaly_df.index, y=anomaly_df[y_column],
        mode='markers',
        marker=dict(color=config['color'],size=3)))

    figure.update_layout(
        xaxis_title='date',
        yaxis_title='value',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return figure
