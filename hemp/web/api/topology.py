from flask_restful import Resource

class Topology(Resource):
    def get(self):
        topologyData = {
            "nodes": [
                {"id": 0, "x": 410, "y": 100, "name": "12K-1"},
                {"id": 1, "x": 410, "y": 280, "name": "12K-2"},
                {"id": 2, "x": 660, "y": 280, "name": "Of-9k-03"},
                {"id": 3, "x": 660, "y": 100, "name": "Of-9k-02"},
                {"id": 4, "x": 180, "y": 190, "name": "Of-9k-01"}
            ],
            "links": [
                {"source": 0, "target": 1},
                {"source": 1, "target": 2},
                {"source": 1, "target": 3},
                {"source": 4, "target": 1},
                {"source": 2, "target": 3},
                {"source": 2, "target": 0},
                {"source": 3, "target": 0},
                {"source": 3, "target": 0},
                {"source": 3, "target": 0},
                {"source": 0, "target": 4},
                {"source": 0, "target": 4},
                {"source": 0, "target": 3}
            ]
        }
        return topologyData

def topology():
    return render_template('topology.html', topo=get_topology_data())
