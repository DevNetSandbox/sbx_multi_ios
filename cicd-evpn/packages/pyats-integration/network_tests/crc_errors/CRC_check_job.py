# To run the job:
# easypy CRC_check_job.py -testbed_file <testbed_file.yaml>
# Description: This job file shows the Genie CRC Interface Checker
import os
from ats.easypy import run


# All run() must be inside a main function
def main():
    # Find the location of the script in relation to the job file
    test_dir = os.path.dirname(__file__)
    crc_tests = os.path.join(test_dir, 'CRC_Count_check.py')
    # Execute the testscript
    run(testscript=crc_tests)
