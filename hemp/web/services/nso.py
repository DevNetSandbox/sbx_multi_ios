import os
import requests
from base64 import b64encode
from flask import render_template

BASE_URL = os.getenv("NSO_URL", "http://localhost:8080")
API_ROOT = BASE_URL + '/api/running'

NSO_USERNAME = os.getenv("NSO_USERNAME", "admin")
NSO_PASSWORD = os.getenv("NSO_PASSWORD", "admin")

HEADERS = {
    'Content-Type': "application/vnd.yang.data+json",
    'authorization': "Basic {}".format(b64encode(b':'.join((NSO_USERNAME,
                                                            NSO_PASSWORD)
                                                          )
                                                 ).strip()
                                      ),
    'accept': "application/vnd.yang.collection+json"
    }

def send_post(url):
    """
    used to pass through NSO requests
    """
    HEADERS['accept'] = 'application/vnd.yang.data+json'
    if not url.startswith('/'):
        url = "/{}".format(url)
    url = BASE_URL + url
    resp = requests.post(url, headers=HEADERS)
    return resp

def get_configured_vpns():
    HEADERS['accept'] = 'application/vnd.yang.collection+json'
    resp = requests.get(API_ROOT + "/vpn", headers=HEADERS)
    print resp.text
    data = resp.json()
    return data['collection']['vpn:vpn']

def add_vpn(**kwargs):
    payload = render_template('xml/new-vpn.xml', **kwargs)
    xml_headers = HEADERS

    xml_headers['Content-Type'] = "application/vnd.yang.data+xml"
    xml_headers['Accept'] = "application/vnd.yang.data+xml"
    resp = requests.post(API_ROOT, data=payload, headers=xml_headers)
    return (resp, payload)


def get_vpn_details(partner_name):
    HEADERS['accept'] = 'application/vnd.yang.data+json'
    url = API_ROOT + "/vpn/{}".format(partner_name)
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    return data['vpn:vpn']
