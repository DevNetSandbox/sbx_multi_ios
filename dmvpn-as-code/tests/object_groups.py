from genie.utils.config import Config
from genie.utils.diff import Diff
from genie.conf import Genie
from pprint import pprint


golden_access_list = """
access-list OUTSIDE_IN extended permit tcp any object-group DMZ_WEBSERVERS eq ww
"""
golden_object_group = """

object-group network DMZ_WEBSERVERS
 host 10.1.250.11
 host 10.1.250.12
 host 10.1.250.13
"""

config = Config(golden_object_group)
config.tree()
expected_config = config.config


def get_config(uut):
    if not uut.is_connected():
        uut.connect()
    config = Config(uut.execute('show running-config'))
    config.tree()
    return config.config



tb = Genie.init('default_testbed.yaml')
uut = tb.devices.headend1

config_dict = get_config(uut)


try:
    actual_config = config_dict['object-group network DMZ_WEBSERVERS ']
    expected_config = expected_config['object-group network DMZ_WEBSERVERS']
except KeyError:
    print("Config Does not exist")


diff = Diff(expected_config, actual_config)
diff.findDiff()
print(bool(diff))
