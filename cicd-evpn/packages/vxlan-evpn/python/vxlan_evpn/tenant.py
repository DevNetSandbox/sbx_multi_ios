import ncs
from ncs.application import Service
from . import fabric
from .allocation import *
import ipaddress
import sys

class TenantService(Service):
    # Allocate VNIIDs for all segments and for the l3 part
    def allocate_vniid(self, root, service, username):
        vniis = {}
        l3vniid = getvniid(root, service,
                          "/vxlan-tenant:vxlan-tenant[name='{}']".format(service.name),
                          username,
                          service.fabric,
                          '{}*'.format(service.name))

        vniis['*'] = l3vniid
        for s in service.segments:
            vniid = getvniid(root, service,
                              "/vxlan-tenant:vxlan-tenant[name='{}']".format(service.name),
                              username,
                              service.fabric,
                              '{}-{}'.format(service.name , s.name))

            vniis[s.name] = vniid
        return vniis

    # Allocate VLANIDs for all segments and for the l3 part
    def allocate_vlanid(self, root, service, username):
        vlans = {}
        l3vlan = getvlanid(root, service,
                          "/vxlan-tenant:vxlan-tenant[name='{}']".format(service.name),
                          username,
                          service.fabric,
                          '{}*'.format(service.name))

        vlans['*'] = l3vlan
        for s in service.segments:
            vlanid = getvlanid(root, service,
                              "/vxlan-tenant:vxlan-tenant[name='{}']".format(service.name),
                              username,
                              service.fabric,
                              '{}-{}'.format(service.name , s.name))

            vlans[s.name] = vlanid
        return vlans


    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        # Allocate identifiers
        vniis = self.allocate_vniid(root, service, tctx.username)
        self.log.info('vniids: {}'.format(vniis))
        vlans = self.allocate_vlanid(root, service, tctx.username)
        self.log.info('vlans: {}'.format(vlans))


        # Ready to push config
        vars = ncs.template.Variables()
        # Tenant specific settings
        vars.add('VRF', service.name)
        # Hardcoded values
        vars.add('BGP_AS', '65001')
        vars.add('NVE_ID', '1')

        template = ncs.template.Template(service)

        # TODO: We can improve performance if we split into more templates
        touched_devices = set()
        for s in service.segments:
            # Segment specific settings
            if not vlans[s.name]:
                continue
            vars.add('VLAN_ID', vlans[s.name])
            if not vniis[s.name]:
                continue
            vars.add('VNI_ID', vniis[s.name])
            if s.suppress_arp:
                vars.add('SUPPRESS_ARP', s.suppress_arp)
            else:
                vars.add('SUPPRESS_ARP', '')

            if sys.version_info.major > 2:
                net = unicode(s.network)
            else:
                net = s.network

            net = ipaddress.ip_network(net)
            hosts = list(net.hosts())
            gw = '{}/{}'.format(hosts[0],net.prefixlen)
            vars.add('GATEWAY', gw)
            # TODO: Improve support. please?
            mnet = vlans[s.name] // 254
            mip  = vlans[s.name] % 254
            vars.add('MCAST_GROUP', '239.0.{}.{}'.format(mnet, mip))

            for c in s.connection:
                self.log.info("Exploring {} {}/{}".format(s.name,c.leaf,c.iface))
                touched_devices.add(c.leaf)

                vars.add('LEAF', c.leaf)

                vars.add('IF', c.iface)
                if c.mode == 'trunk':
                    vars.add('TRUNK', 'trunk')
                else:
                    vars.add('TRUNK', '')
                self.log.info('VARS: {}'.format(vars))
                template.apply('vxlan-tenant-connection', vars)


        # L3 segment
        for d in touched_devices:
            vars.add('LEAF', d)
            vars.add('VLAN_ID', vlans['*'])
            vars.add('VNI_ID', vniis['*'])
            self.log.info('VARS: {}'.format(vars))
            template.apply('vxlan-tenant-l3', vars)


        # Set VNI/VLAN oper data
        for s in service.segments:
            vni = vniis[s.name]
            if vni:
                s.vni_id = vni

            vlan = vlans[s.name]
            if vlan:
                s.vlan_id = vlan

#

#        self.log.info('Vars', vars)
#
#        template.apply('vxlan-evpn-base', vars)
