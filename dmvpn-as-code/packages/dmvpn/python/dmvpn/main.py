# -*- mode: python; python-indent: 4 -*-
import ncs
from .dmvpn import DMVPN
from .actions import DMVPNAction


class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('dmvpn-servicepoint', DMVPN)
        self.register_action('dmvpn-action', DMVPNAction)

    def teardown(self):

        self.log.info('Main FINISHED')
