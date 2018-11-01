from flask import Flask, render_template, request
from flask_restful import Api
from views.topology import topology
from views.monitoring import monitoring
from views.vpn import vpn_list, add_vpn, vpn_detail
from views.patterns import patterns
from api.vpn import VPN
from api.nso import NSOPassthrough
from api.topology import Topology

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(VPN, '/api/vpn')
api.add_resource(NSOPassthrough, '/nso/<path:nso_url>')
api.add_resource(Topology, '/api/topology')
app.add_url_rule('/topology', endpoint='topology-view', view_func=topology)
app.add_url_rule('/vpn', endpoint='vpn-list', view_func=vpn_list)
app.add_url_rule('/vpn/<string:partner_name>', endpoint='vpn-detail', view_func=vpn_detail)
app.add_url_rule('/vpn/add', endpoint='add-vpn', methods=["GET", "POST"], view_func=add_vpn)
app.add_url_rule('/monitoring', endpoint='monitoring', view_func=monitoring)
app.add_url_rule('/patterns', endpoint='patterns', view_func=patterns)

if __name__ == '__main__':
    app.secret_key = "23lk4jwfsaduljk5q3rauFjklsdjafslkej5rZX"
    app.run(host='0.0.0.0', port=5000, debug=True)
