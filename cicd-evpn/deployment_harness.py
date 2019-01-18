'''Genie deployment harness for Ansible Playbook
'''
import os
from ats.datastructures.logic import And, Not, Or
from genie.harness.main import gRun
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--playbook',
                        dest='playbook',
                        default='site.yaml')
    parser.add_argument('--inventory',
                        dest='inventory',
                        default='inventory/test.yaml')
    args, unknown = parser.parse_known_args()

    test_path = os.path.dirname(os.path.abspath(__file__))
    print(args)
    # mapping_datafile is mandatory
    # trigger_uids limit which test to execute
    gRun(mapping_datafile=os.path.join(test_path, 'tests/profile/mapping_datafile.yaml'),
         trigger_datafile='tests/profile/trigger_datafile.yaml',
         pts_datafile='tests/profile/pts_datafile.yaml',
         pts_features=['ospf', 'bgp'],
         playbook=args.playbook,
         inventory=args.inventory,
         trigger_uids=Or('RunAnsiblePlaybook'))
