""""
Simple Genie Script

"simpler is better than complex"

pyATS + Genie provide a lot of framework that you can use if you desire, it can
be a bit overwhelming at first...

This is a simple test to determine that HSRP is active on all interfaces
that it is running on a.k.a the "primary" device

More Info:
https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/Ops/user/ops.html#introduction

"""
import sys
from genie.conf import Genie
# import the topology module
from ats.topology import loader

# you're gonna love Lookup
from genie.abstract import Lookup

# gotcha: if your linitng you code this may raise an error but is necessary
# it's not used until we perform a lookup
from genie.libs import ops # noqa

# load testbed file which describes our devices
pyats_testbed = loader.load('../test_testbed.yml')
# pyats testbed != genie testbed
genie_testbed = Genie.init(pyats_testbed)

# pick a device from the testbed
dist1 = genie_testbed.devices['dist1']
dist1.connect()

# dist1 is now your connection to the device
# what do you want to do?

# dist1.execute('show version')
# dist1.configure('ip domain-name netdevlops.com')
# dist1.ping('192.168.0.1')

# but if you were interested in running CLI, you wouldnt be using pyATS,
# so we might as well use genie while we're at it...

# perform a lookup to identify the device, this identifies the os type based on
# the testbed definition:
# custom:
#  abstraction:
#   order: [os, type]

# https://pubhub.devnetcloud.com/media/pyats-packages/docs/abstract/lookup_class.html
lookup = Lookup.from_device(dist1)

# learn the operational state of hsrp on the device
hsrp = lookup.ops.hsrp.hsrp.Hsrp(device=dist1)
hsrp.learn()

# the results are stored in a hsrp.info dictionary whose keys are
# interface names
#
# full documentation for the hsrp schema:
# https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/_models/hsrp.pdf

# get/track hsrp states
group_states = list()
for interface in hsrp.info:
    details = hsrp.info[interface]
    v1_groups = details['address_family']['ipv4']['version'][1]['groups']
    for id, grp_detail in v1_groups.items():
        state = grp_detail['hsrp_router_state']
        print("Interface {} is {}".format(interface, state))
        group_states.append(state)

# all hsrp groups should be active
if all([state == 'active' for state in group_states]):
    print("HSRP is active on all interfaces")

# if not we fail the test
elif all([state == 'standby' for state in group_states]):
    print("HSRP is standby on all interfaces")
    sys.exit(1)

# that wasnt so bad was it?
