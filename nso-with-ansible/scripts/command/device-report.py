#!/usr/bin/env python
import sys
import argparse
import os
import subprocess
import ncs
import _ncs
import ncs.maagic as maagic

step = 1
services = []
port = 0
devcfg = ""
NO_NETWORKING = (1 << 4)


def print_ncs_command_details():

    cli_doc = """
        begin command
            modes: oper
            styles: c i j
            cmdpath: device-report
            help: Generate a Device Config for Ansible
        end
        begin param
          name: device
          presence: mandatory
          flag: -d
          help: Device to generate
        end
    """
    print(cli_doc)


def devExists(t, devName):
    path = '/ncs:devices/device{"' + devName + '"}'
    if (t.exists(path)):
        return True
    return False


def getDeviceObject(dev_name):
    """
    returns device object for `dev_name`
    """
    print('getting device info for {}'.format(dev_name))
    m = ncs.maapi.Maapi()
    m.start_user_session('admin', 'system', [])
    trans = m.start_read_trans()
    root = ncs.maagic.get_root(trans)
    return root.devices.device[dev_name]


def main(argv):

    global services
    global port
    global devcfg
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", action='store_true',
                        dest='command', help="command")
    parser.add_argument("-d", "--device", action='store',
                        dest='src', help="device to generate")
    parser.add_argument("-v", "--verbose", action='store',
                        dest='verbose', help="device to generate")
    args = parser.parse_args()

    if args.command:
        print_ncs_command_details()
        exit(0)

    print("\nDoing Some command script stuff with [%s] ....\n" % (args.src))
    device = getDeviceObject(args.src)
    msg = """
    Device Name: {}
    Device NED: {}
    Device IP: {}
    """.format(device.name, device.device_type.cli.ned_id, device.address)
    print(msg)


if __name__ == '__main__':
    main(sys.argv[1:])
