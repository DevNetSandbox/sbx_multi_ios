import os
from ats.easypy import run


# All run() must be inside a main function
def main():
    # Find the location of the script in relation to the job file
    test_dir = os.path.dirname(__file__)
    bgp_tests = os.path.join(test_dir, 'BGP_Neighbors_Established.py')
    # Execute the testscript
    run(testscript=bgp_tests)
