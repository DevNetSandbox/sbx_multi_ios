#!/bin/env python

# To get a logger for the script
import logging

# Needed for aetest script
from ats import aetest
# import the genie libs
from genie.libs import ops # noqa

# import our customer parsers
from parsers.eigrp import show_ip_eigrp_neighbors

# Get your logger for your script
log = logging.getLogger(__name__)


class EIGRP_Neighbor_Count(aetest.Testcase):
    """ This is user Testcases section """

    @aetest.test
    def connect(self, testbed, device, expected_nbr_count):
        log.info("Connecting to {}".format(device))
        d = testbed.devices[device]
        d.connect()

    @aetest.test
    def count(self, testbed, device, expected_nbr_count):
        device_nbrs = show_ip_eigrp_neighbors(testbed.devices[device])
        log.info(device_nbrs)
        nbr_count = len(device_nbrs)
        if int(nbr_count) == int(expected_nbr_count):
            self.passed()
        else:
            msg = '{} has {} neigbors, expected {}'
            fail_msg = msg.format(device, nbr_count, expected_nbr_count)
            self.failed(fail_msg)


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
