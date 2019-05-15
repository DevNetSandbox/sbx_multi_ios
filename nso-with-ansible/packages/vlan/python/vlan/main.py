# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class VLANService(Service):
    """
    This class represents the logic required to provision a VLAN
    """
    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Creating VLAN {} (id {})'.format(service._path,
                                                        service.id))

        vars = ncs.template.Variables()

        template = ncs.template.Template(service)
        template.apply('vlan-template', vars)

        # apply template to access ports in this vlan
        self.log.info('Configuring Access ports for VLAN {}'
                      .format(service.id)
                      )
        template.apply('access-port-template')

        # apply template to trunk ports in this vlan
        self.log.info('Configuring Trunk ports for VLAN {}'.format(service.id))
        template.apply('trunk-port-template')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Launching VLAN Automation service')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding YANG model.
        self.register_service('vlan-servicepoint', VLANService)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.
        self.log.info('Shutting down VLAN Automation service')
