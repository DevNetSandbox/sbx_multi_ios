import os
from ats.easypy import run
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', dest='device')
    parser.add_argument('--nbr-count', dest='expected_nbr_count')
    args, unknown = parser.parse_known_args()
    pwd = os.path.dirname(__file__)
    eigrp = os.path.join(pwd, 'EIGRP_TestCases.py')
    run(testscript=eigrp, **vars(args))
