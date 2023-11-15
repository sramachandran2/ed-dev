import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/d3/4.1.1/d3.js'],
)
