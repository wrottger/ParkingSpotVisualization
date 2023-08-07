# app.py

import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
from PIL import Image

data = (
    pd.read_csv("avocado.csv")
    .query("type == 'conventional' and region == 'Albany'")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

app = Dash(__name__)

parking_spots = [
    {'x': 88, 'y': 70, 'occupied': 0},
    {'x': 136, 'y': 70, 'occupied': 1},
    {'x': 183, 'y': 70, 'occupied': 1},
    {'x': 230, 'y': 70, 'occupied': 0},
    {'x': 275, 'y': 70, 'occupied': 0},
    {'x': 323, 'y': 70, 'occupied': 0},
    {'x': 88, 'y': 223, 'occupied': 1},
    {'x': 136, 'y': 223, 'occupied': 0},
    {'x': 183, 'y': 223, 'occupied': 1},
    {'x': 230, 'y': 223, 'occupied': 1},
    {'x': 275, 'y': 223, 'occupied': 0},
    {'x': 323, 'y': 223, 'occupied': 1},
]

map_fig = go.Figure()

parking_image = Image.open("parking_spot.jpg")


# Add the map image as a static background image
map_fig.add_layout_image(
    source=parking_image,
    x=0,
    y=0,
    xref="x",
    yref="y",
    sizex=360,  # Adjust the size as needed
    sizey=294,  # Adjust the size as needed
    sizing="stretch",
    opacity=1,
    layer="below",
)

for spot in parking_spots:
    if spot['occupied'] == 1:
        color = 'red'  # Occupied spots will be shown in red
    else:
        color = 'green'  # Empty spots will be shown in green

    map_fig.add_trace(go.Scatter(
        x=[spot['x']],
        y=[spot['y']],
        mode='markers',
        marker=dict(size=10, color=color),
        showlegend=False
    ))

map_fig.update_layout(
    xaxis=dict(range=[0, 360]),  # Adjust the range based on your image size
    yaxis=dict(range=[0, 294]),  # Adjust the range based on your image size
)

app.layout = html.Div(
    children=[
        html.H1(children="Smart City Dashboard"),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Freie Parkplätze"},
            },
        ),
        dcc.Graph(
            id='map-plot',
            figure=map_fig

        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
