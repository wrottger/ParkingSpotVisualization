from PIL import Image
import json
from parkingspots import ParkingSpots

import dash
from dash import Dash, dcc, html, Input, Output, callback

# Init parking graph


# Init parking spot images
parking_image = Image.open("assets/parking_spot.jpg")
with open("assets/parking_spots.json") as parking_file:
    parking_data = json.load(parking_file)
parking_fig = ParkingSpots(parking_image, parking_data)
parking_fig.update_spots()

# Init Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Freie Parkplätze'),
        dcc.Graph(
            figure=parking_fig.fig,
            config={
               'displayModeBar': False
            }
            ),
    ])
)

if __name__ == '__main__':
    app.run(debug=True)
