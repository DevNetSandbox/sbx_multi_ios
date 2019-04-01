from flask_restful import Resource

class Device(Resource):
    def get(self):
        devices = [
            {"hostname": "router1",
             "ip_address": "1.1.1.1",
             "model": "Catalyst 9300",
             "version": "15.1",
            },
            {"hostname": "router2",
             "ip_address": "2.2.2.2",
             "model": "Catalyst 9300",
             "version": "15.1",
            }
        ]
        return devices
