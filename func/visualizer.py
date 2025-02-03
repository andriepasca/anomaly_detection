import plotly.graph_objects as go


def plot_base_line(df,y_column):
    figure = go.Figure()
    figure.add_trace(go.Scatter(name=y_column, x = df.index, y=df[y_column], marker=dict(color='rgba(50,50,50,0.3)')))
    return figure

def plot_anomalies(df, y_column, anomaly_type):
    figure = go.Figure()
    if anomaly_type == 'levelshift':
        config={
            'anomaly_column':'levelshift_ad',
            'legend_name': 'levelshift anomaly',
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
        marker=dict(color=config['color'],size=4)))

    figure.update_layout(
            xaxis_title='date',
            yaxis_title='value',
            legend_title="Anomaly Type",
        )

    return figure


def plot(df, y_column, configs):
    figure = go.Figure()
    configs=[
        {
            'anomaly_column':'levelshift_ad',
            'legend_name':'Level shift warning',
            'conditions':{
                'levelshift_ad':True,
                'isolation_ad':False,
            },
            'style':{
                'color': 'rgba(249,123,34,0.8)',
                'marker_size': 4
            }
        },
        {
            'anomaly_column':'isolation_ad',
            'legend_name':'Collective warning',
            'conditions':{
                'levelshift_ad':False,
                'isolation_ad':True,
            },
            'style':{
                'color': 'rgba(255,217,61,0.8)',
                'marker_size': 4
            }
        },
        {
            'legend_name':'Overlap warning',
            'conditions':{
                'levelshift_ad':True,
                'isolation_ad':True,
            },
            'style':{
                'color': 'rgba(223,46,56,0.8)',
                'marker_size': 4
            }
        },
    ]
    # plot baseline
    figure.add_trace(go.Scatter(name=y_column, x = df.index, y=df[y_column], marker=dict(color='rgba(50,50,50,0.3)')))

    # plot both levelshift and collective anomalies
    for config in configs:
        anomaly_df = df
        for anomaly_type, status in config['conditions'].items():
            anomaly_df = anomaly_df[anomaly_df[anomaly_type]==status]

        figure.add_trace(go.Scatter(name=config['legend_name'], x = anomaly_df.index, y=anomaly_df[y_column],
            mode='markers',
            marker=dict(color=config['style']['color'],size=4)))

        figure.update_layout(
            title= 'DAU (simulated)',
            xaxis_title='date',
            yaxis_title='DAU',
            legend_title="Anomaly Type",
        )

    return figure
