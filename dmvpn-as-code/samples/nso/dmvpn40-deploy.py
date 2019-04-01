import requests
import json
import yaml
from requests.auth import HTTPBasicAuth

url = "http://localhost:8080/api/running/"

with open('dmvpn40.yaml') as fh:
    payload = yaml.load(fh)

headers = {
    'Content-Type': "application/vnd.yang.data+json",
    'Accept': "application/vnd.yang.data+json, application/vnd.yang.collection+json,application/vnd.yang.datastore+json",
    }

response = requests.post(url,
                         auth=HTTPBasicAuth('admin', 'admin'),
                         data=json.dumps(payload),
                         headers=headers)
print("Status Code: {}".format(response.status_code))
print(response.text)
