

import dash
import dash_html_components as html
from commons import app

app_dash = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/'
)

app_dash.layout = html.Div("My Dash app")
