# app.py
from random import random

import PIL.Image
import plotly
from PIL import Image
import json
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from collections import deque


# Init parking spot image
parking_image = Image.open("assets/parking_spot_image.png")

# Init Dash app
app = Dash(__name__, title='Weekly Analytics', update_title=None, external_stylesheets=[dbc.themes.LUX])

layout = html.Div([
    html.H1("Freie Parkplätze",
            style={"margin-top": "15px", "margin-left": "15px"}),
    html.Div(children=[
        dcc.Graph(
            config={
                'displayModeBar': False
            },
            id='free-spots',
            style={'display': 'inline-block'}
        ),
        dcc.Graph(
            config={
                'displayModeBar': False
            },
            id='parking-spot-graph',
            style={'display': 'inline-block'}
        )],
        style={"margin": "0px"}),
    dcc.Interval(
        id='interval-component',
        interval=1 * 500,  # in milliseconds
        n_intervals=0
    ),
]
)

app.layout = layout


def import_parking_status():
    with open("hall_effect_scripts/output/status.csv", "r") as f:
        string_values = f.readline().split(sep=", ")
    return list(map(int, string_values))


@callback(Output('free-spots', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_spots(n):
    img = PIL.Image.open("assets/parking_spot_image.png")
    fig = px.imshow(img)
    fig.update_layout(
        margin=dict(l=30, r=0, b=0, t=0),
        width=445,
        height=400
    )
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

historical_status = deque( maxlen=30 )
@callback(Output('parking-spot-graph', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_graph(n):
    fig = px.line()
    fig.update_layout(
        margin=dict(l=30, r=0, b=0, t=0),
        width=445,
        height=400,

    )
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)

    spots = import_parking_status()
    occupied_spots = spots.count(1)
    historical_status.append(random() * 5)
    trace = plotly.graph_objs.Scatter(
        x=[i for i in range(30)],
        y=list(historical_status),
        )
    return {'data': [trace]}


if __name__ == '__main__':
    app.run(debug=True)
