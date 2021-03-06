from commons.db import Session
from commons.mapped_classes import *
from commons.fetch_data import *
from commons.data_exploration import *
from flask import Flask, redirect, request
from flask_cors import CORS
from commons import *
from commons.populate_db import *
import json



app = Flask(__name__)
CORS(app)



@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()


@app.route('/', methods=['GET'])
def vis_data():
    mps = Session.query(MP).filter(MP.person_id.in_(mps_current()))

    frame, _ = cluster_mps(mps,5,eu_divisions)

    frame.sort_values("party",inplace=True)
    # nodes_frame =  add_master_nodes(frame)
    pack_data =  frame.to_dict(orient='records')
    _, new_nodes = add_master_nodes(frame)
    pack_data = pack_data + new_nodes

    divisions = Session.query(Division).filter(Division.division_number.in_(eu_divisions))
    bar_data = [div2dict(div) for div in divisions]
    return json.dumps([pack_data, bar_data])



@app.route('/cluster', methods=['GET'])
def cluster():
    mps = Session.query(MP).filter(MP.person_id.in_(mps_current()))
    frame, _ = cluster_mps(mps,5,eu_divisions)
    frame.sort_values("party",inplace=True)
    # nodes_frame =  add_master_nodes(frame)
    clustered_mps = frame.to_dict(orient='records')

@app.route('/plotly_dashboard')
def render_dashboard():
    return redirect('/dash/')


''' Dash App '''

# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# import dash_table



# app_dash = dash.Dash(
#     __name__,
#     server=app,
#     routes_pathname_prefix='/dash/'
# )

# divs = Session.query(Division)
# divs = query2df(divs)

# app_dash.layout = html.Div(children=[
#                 html.Div(id='bar_chart_div'),
#                 html.Div([
#                 dash_table.DataTable(
#                     id='datatable-interactivity',
#                     columns=[
#                         {"name": i, "id": i, "deletable": True, "selectable": True} for i in divs.columns
#                     ],
#                     data=divs.to_dict('records'),
#                     edpiitable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     column_selectable="single",
#                     row_selectable="multi",
#                     row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10,
#                 ),
#                 html.Div(id='datatable-interactivity-container')
#             ])
#             ])

# @app_dash.callback(
# Output(component_id='bar_chart_div', component_property='children'),
# [Input(component_id='divs-dropdown', component_property='value')]
# )
# def draw_bar_chart(div_num):

#     div_num = int(div_num)
#     div = Session.query(Division)\
#                   .filter(Division.division_number==div_num).one()

#     division = div2dict(div)
#     X = ['ayes', 'noes', 'abstentions']
#     Y = [division[x] for x in X]

#     bar = go.Bar(x=X,y=Y)

#     return dcc.Graph(
#         id='bar_chart',
#         figure={
#             'data': [bar],
#             'layout':{'title':division['title']}
#         }
#     )

