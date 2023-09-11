import dash
import PIL.Image
import pandas as pd
import json
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from collections import deque

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H3('Parkplatz Dashboard'),
    html.Div([
        html.Div([
            dcc.Graph(
                config={
                    'displayModeBar': False
                },
                id='free-spots',
                responsive=False,
            ),
        ], className="six columns"),
        html.Div([
            dcc.Graph(
                config={
                    'displayModeBar': False
                },
                id='parking-spot-graph',
                responsive=True,
            ),
        ], className="six columns"),
    ], className="row"),
    dcc.Interval(
        id='interval-component',
        interval=1 * 500,  # in milliseconds
        n_intervals=0
    ),
])


def import_parking_status():
    with open("hall_effect_scripts/output/status.csv", "r") as f:
        string_values = f.readline().split(sep=", ")
    return list(map(int, string_values))


@callback(Output('free-spots', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_spots(n):
    img = PIL.Image.open("assets/parking_spot_image.png")
    fig = px.imshow(img, title="<br>            Karte")
    with open("assets/parking_spots.json", "r") as f:
        coords = json.load(f)
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)

    spots = import_parking_status()
    for idx, spot in enumerate(spots):
        if spot == 1:
            color = '#FF2400'
        else:
            color = 'lawngreen'
        fig.add_trace(go.Scatter(
            x=[coords[idx]['x']],
            y=[coords[idx]['y']],
            mode='markers',
            marker=dict(size=10, color=color),
            hoverinfo='none',
            showlegend=False
        ))
    return fig


historical_status = deque(maxlen=500)


@callback(Output('parking-spot-graph', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_graph(n):
    spots = import_parking_status()
    occupied_spots = spots.count(1)
    historical_status.append(occupied_spots)
    df = pd.DataFrame(dict(
        y=list(historical_status),
    ))

    fig = px.area(df, title="<br>            Besetzte Parkplätze")
    fig.update_xaxes(showticklabels=False, )
    fig.update_layout(showlegend=False,
                      yaxis_title=None,
                      xaxis_title=None,
                      yaxis=dict(range=[0, 16]))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
