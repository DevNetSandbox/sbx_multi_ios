# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service

from . import leaf
from . import spine
from . import fabric
from . import tenant

# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('vxlan-evpn-fabric', fabric.FabricService)
        self.register_service('vxlan-evpn-leaf', leaf.LeafService)
        self.register_service('vxlan-evpn-spine', spine.SpineService)
        self.register_service('vxlan-evpn-tenant', tenant.TenantService)

        self.register_action('vxlan-fabric-verify', fabric.Verify)


    def teardown(self):
        self.log.info('Main FINISHED')
