import ncs
from ncs.application import Service
from . import allocation
from .remote import remote_configuration
from .headend import headend_configuration


class DMVPN(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        # Allocate any required IP addresses
        tunnel_ips = allocation.allocate_tunnel_ips(root,
                                                    service,
                                                    tctx.username,
                                                    self.log)
        self.log.info('Tunnel IPs: {}'.format(tunnel_ips))

        lan_networks = allocation.allocate_lan_networks(root,
                                                        service,
                                                        tctx.username,
                                                        self.log)
        self.log.info('LAN Networks: {}'.format(lan_networks))

        # No point in proceeding until at least some allocation is done
        if tunnel_ips is None:
            self.log.warning('No allocations yet')
            return
        
        headend_configuration(service, tunnel_ips, self.log)
        remote_configuration(service, tunnel_ips, lan_networks, self.log)
