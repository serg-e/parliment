from flask import Flask
from flask_cors import CORS
from commons import *
import json



app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()


@app.route('/', methods=['GET'])
def cluster():
    mps = Session.query(MP).all()
    frame, _ = cluster_mps(mps,5,eu_divisions)
    frame.sort_values("party",inplace=True)
    # nodes_frame =  add_master_nodes(frame)
    pack_data =  frame.to_dict(orient='records')
    _, new_nodes = add_master_nodes(frame)
    pack_data = pack_data + new_nodes

    divisions = Session.query(Division).filter(Division.division_number.in_(eu_divisions))
    bar_data = [div2dict(div) for div in divisions]

    return json.dumps([pack_data, bar_data])
#
# test = list(cluster())
#
# test[55000:55070]
