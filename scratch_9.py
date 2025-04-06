
import dash
from dash import dcc, html
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("My Dash App"),
    dcc.Graph(figure={
        "data": [{"x": [1, 2, 3], "y": [4, 1, 2], "type": "line", "name": "Sample"}],
        "layout": {"title": "Sample Graph"}
    })
])

if __name__ == "__main__":
    app.run_server(debug=True)
