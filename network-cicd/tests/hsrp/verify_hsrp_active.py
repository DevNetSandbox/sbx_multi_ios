""""
Simple Genie TestCase

"complex is better than complicated"

pyATS + Genie provide a lot of framework that you can use if you desire, but
it can be a bit overwhelming at first...

In this example, we'll use a bit more of the pyATS framework

    AEtest (Automation Easy Testing) a.k.a "test harness"
    It offers a simple and straight-forward way for
    users to define, execute and debug testcases and testscripts,
    serving as a basis for other testscript templates & engines.


TRANSLATION: it knows you want to test something and handles all of the
pass/fail/grouping/tracking stuff you'd like to do and gives you pretty console
output

More Info:
https://pubhub.devnetcloud.com/media/pyats/docs/aetest/introduction.html

"""
import re
import logging

from ats import aetest
from ats.log.utils import banner

# genie libraries
from genie.conf import Genie
from genie.abstract import Lookup
from genie.libs import ops # noqa


# create a logger for this testscript
logger = logging.getLogger(__name__)


class common_setup(aetest.CommonSetup):
    '''Common Setup Section
    stuff you only wanna do once
    '''

    @aetest.subsection
    def validate_testbed(self, testbed):

        '''
        basic checks of the testbed file
        '''
        # abort/fail the testscript if no testbed was provided
        if not testbed or not testbed.devices:
            self.failed('No testbed was provided to script launch',
                        goto=['exit'])

        # abort/fail the testscript if no matching device was provided
        if 'dist1' not in testbed:
            self.failed('testbed needs to contain device `dist1`',
                        goto=['exit'])

        genie_testbed = Genie.init(testbed)
        dist1 = genie_testbed.devices['dist1']

        # add device to testscript parameters so we can use it later
        self.parent.parameters.update(dist1=dist1)

    @aetest.subsection
    def establish_connections(self, steps, dist1):


        # first step, connect to the device
        with steps.start('Connecting to dist1'):
            dist1.connect()

        # abort/fail the testscript if we can't connect
        if not dist1.connected:
            self.failed('Could not connect',
                        goto=['exit'])


class VerifyHSRPActive(aetest.Testcase):
    '''Verifies that HSRP is active test'''

    @aetest.test
    def learn_about_hsrp(self, dist1):

        # this can be wrapped in an try/except block to differentiate between
        # test failed or script died...
        try:

            lookup = Lookup.from_device(dist1)
            hsrp = lookup.ops.hsrp.hsrp.Hsrp(device=dist1)
            hsrp.learn()

        except Exception as e:
            # abort/fail on any exception
            # such as connection timeout or command failure
            self.failed('Error trying learn hsrp - error: {}'.format(e),
                        goto=['exit'])

    @aetest.setup
    def setup(self, dist1):

        # this can be wrapped in an try/except block to differentiate between
        # test failed or script died...
        try:

            lookup = Lookup.from_device(dist1)
            hsrp = lookup.ops.hsrp.hsrp.Hsrp(device=dist1)
            hsrp.learn()

            # update testcase
            self.hsrp_info = hsrp.info

        except Exception as e:
            # abort/fail on any exception
            # such as connection timeout or command failure
            self.failed('Error trying learn hsrp - error: {}'.format(e),
                        goto=['exit'])

    @aetest.test
    def verify_all_active(self):
        try:
            group_states = list()
            for interface in self.hsrp_info:
                details = self.hsrp_info[interface]
                v1_groups = details['address_family']['ipv4']['version'][1]['groups']
                for id, grp_detail in v1_groups.items():
                    state = grp_detail['hsrp_router_state']
                    logger.debug("Interface {} is {}".format(interface, state))
                    group_states.append(state)

            # all hsrp groups should be active
            if all([state == 'active' for state in group_states]):
                logger.info("HSRP is active on all interfaces")
            else:
                self.failed('Not all hsrp interfaces are active')

        except Exception as e:
            self.failed("Encountered an exception: {}".format(e))


class common_cleanup(aetest.CommonCleanup):
    '''disconnect from ios routers'''

    @aetest.subsection
    def disconnect(self, steps, dist1):
        '''disconnect from both devices'''

        with steps.start('Disconnecting from dist1'):
            dist1.disconnect()


if __name__ == '__main__':

    # local imports
    import argparse
    from ats.topology import loader

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument('--testbed', dest='testbed', type=loader.load)
    # parse args
    args, unknown = parser.parse_known_args()

    # and pass all arguments to aetest.main() as kwargs
    aetest.main(**vars(args))
