from flask import Flask
from flask_cors import CORS
from commons import *
import json



app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()
    print('Session removed')

@app.route('/', methods=['GET'])
def index():
    mps = Session.query(MP).all()
    frame, _ = cluster_mps(mps,4,eu_divisions)
    nodes_frame =  add_master_nodes(frame)
    return nodes_frame.to_json(orient='records')
