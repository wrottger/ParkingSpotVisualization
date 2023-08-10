import plotly.express as px
import plotly.graph_objects as go


class ParkingSpots:

    def __init__(self, img, spots):
        self.spots = spots
        self.fig = px.imshow(img)
        self.fig.update_layout(
            width=400,
            height=400,
            margin=dict(l=10, r=10, b=10, t=10),
        )
        self.fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)

    def update_spots(self):
        for spot in self.spots:
            if spot['occupied'] == 1:
                color = '#FF2400'  # Occupied spots will be shown in red
            else:
                color = 'lawngreen'  # Empty spots will be shown in green
            self.fig.add_trace(go.Scatter(
                x=[spot['x']],
                y=[spot['y']],
                mode='markers',
                marker=dict(size=10, color=color),
                hoverinfo='none',
                showlegend=False
            ))
