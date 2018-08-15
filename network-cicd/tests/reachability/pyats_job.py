#!/bin/env python

'''pyats_ios_example_job.py

This is an easypy job example intended to run the pyATS IOS example testscript.


Arguments:
    This script requires one script argument (testbed_file) and two optional
    script argument (ios1 and ios2) to be passed in when run under easypy for
    demonstration purposes.
    testbed_file: the path to testbed yaml file
    ios1: the device name defined in the testbed yaml file, if modified
    ios2: the device name defined in the testbed yaml file, if modified

Examples:
    # to run under easypy
    bash$ easypy pyats_ios_example_job.py -testbed_file pyats_ios_example.yaml

References:
   For the complete and up-to-date user guide on pyATS, visit:
    https://developer.cisco.com/site/pyats/docs/
'''

#
# optional author information
#
__author__ = 'Wei Chen <weiche3@cisco.com>'
__copyright__ = 'Copyright 2017, Cisco Systems'
__email__ = 'pyats-support@cisco.com'
__date__= 'Nov 15, 2017'


#
# import statements
#
import os
import logging
import argparse

from ats.easypy import run


def main():

    # parse args

    # configure your log outputs level
    #logging.getLogger('ats.connections').setLevel('DEBUG')

    # Find the location of the script in relation to the job file
    test_path = os.path.dirname(os.path.abspath(__file__))
    testscript = os.path.join(test_path, 'pyats_loopback_reachability.py')

    # run it
    run(testscript)
