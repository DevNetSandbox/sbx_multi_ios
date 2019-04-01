from flask_restful import Resource

if __name__ == '__main__':
    if __package__ is None:
        sys.path.append(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

from services.nso import get_configured_vpns

class VPN(Resource):
    def get(self):
        return get_configured_vpns()
