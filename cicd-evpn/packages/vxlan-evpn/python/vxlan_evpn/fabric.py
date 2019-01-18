import ncs
from ncs.application import Service
from ncs.dp import Action
import ipaddress
from .allocation import *
import ncs.maapi as maapi
import ncs.maagic as maagic
import re

try:
    unicode = str
except:
    pass


def get_ip(ipandmask):
    ip = ipandmask.split('/')[0]
    return ip

# Count number of OSPF neighbours
def countosfp(r):
    cnt = 0
    for l in r.result.split('\n'):
        if 'FULL' in l:
            cnt += 1
    return cnt

# Count number of BGP neighbours
def countbgp(r):
    state = 0
    cnt = 0
    for l in r.result.split('\n'):
        if state == 0 and 'Neighbor' in l:
            state = 1
            continue
        if state == 1:
            try:
                (ip, v, asnum, rcvd, send, tail) = re.split('\s+', l, 5)
                if int(rcvd) > 0 and int(send) > 0:
                    cnt += 1
            except ValueError:
                state = 2
    return cnt

# Check status for a single device
def checkdev(devs, devname, lbl, num):
    show = devs[devname].live_status.__getitem__('exec').show #.exec.show
    inp = show.get_input()

    # Check OSPF settings
    inp.args = ['ip ospf neigh']
    r = show.request(inp)
    #self.log.info('Show OSPF: {}'.format(r.result))
    ospfcnt = countosfp(r)

    # Check BGP
    inp.args = ['ip bgp all summary']
    r = show.request(inp)
    bgpcnt = countbgp(r)

    # Check that the spine had everything
    if ospfcnt == num and bgpcnt == num:
        rs = 'READY'
    else:
        rs = 'NOT READY'
        allOk = False

    return '{} {}, OSPF status: {}/{}, BGP STATUS: {}/{} - {}\n'.format(lbl, devname, ospfcnt, num, bgpcnt, num, rs)

class Verify(Action):
    @Action.action
    def cb_action(self, uinfo, _name, kp, input, output):
        result = ''
        self.log.info('VXLAN Fabric Verify for {}'.format(kp))
        allOk = True
        with maapi.single_read_trans(uinfo.username, 'vxlan-verify') as cfg:
            svc = maagic.get_node(cfg, kp)
            root = ncs.maagic.get_root(cfg)
            devs = root.devices.device
            numleafs = len(svc.leaves)
            numspines = len(svc.spines)

            self.log.info('Fabric: {}, spines: {}, leafs: {}'.format(svc.name, numspines, numleafs))

            # Check all spines
            for s in svc.spines:
                result += checkdev(devs, s.device, 'Spine', numleafs)
            for l in svc.leaves:
                result += checkdev(devs, l.device, 'Leaf', numspines)

        if allOk:
            result += 'SUMMMARY: BGP AND OSPF OK\n'
            output.ready = True
        else:
            result += 'SUMMARY: NOT READY\n'
            output.ready = False
        output.result = result

class FabricService(Service):

    # Allocate PIM addresses for everyone (loopback1)
    def allocate_pim(self, root, service, username):
        vars = ncs.template.Variables()
        pim = service.pim_pool
        vars.add('POOL_NAME', getpimpool(service))
        vars.add('PREFIX', pim.split('/')[0])
        vars.add('PREFIX_LEN', pim.split('/')[1])
        template = ncs.template.Template(service)
        template.apply('vxlan-pool-create', vars)

        globalpim = None
        pimips = {}

        # Now go through all spines and allocate their pim-ids
        globala = '{}*'.format(service.name)
        globalpim = getpimip(root, service, username, globala)
        pimips[globala] = globalpim

        # Then go through all leaves and allocate their pim-ids
        for s in service.leaves:
            pimip = getpimip(root, service, username, s.device)
            if not(pimip is None):
                pimips[s.device] = pimip
            isFirst = False

        return (globalpim, pimips)

    # Allocate loopback0 addresses for everyone
    def allocate_loopbacks(self, root, service, username):
        loopb = service.loopback_pool
        vars = ncs.template.Variables()
        vars.add('POOL_NAME', getlooppool(service))
        vars.add('PREFIX', loopb.split('/')[0])
        vars.add('PREFIX_LEN', loopb.split('/')[1])
        template = ncs.template.Template(service)
        template.apply('vxlan-pool-create', vars)

        loopbackips = {}
        # First the spines
        for s in service.spines:
            loopip = getloopip(root, service, username, s.device)
            if not(loopip is None):
                loopbackips[s.device] = loopip
        # Then the leaves
        for s in service.leaves:
            loopip = getloopip(root, service, username, s.device)
            if not(loopip is None):
                loopbackips[s.device] = loopip
        return loopbackips

    # Allocate interior nets for all links from a spine to a leaf
    def allocate_interior(self, root, service, username):
        vars = ncs.template.Variables()
        intpool = service.interior_pool
        vars.add('POOL_NAME', getintpool(service))
        vars.add('PREFIX', intpool.split('/')[0])
        vars.add('PREFIX_LEN', intpool.split('/')[1])
        template = ncs.template.Template(service)
        template.apply('vxlan-pool-create', vars)

        intlinks = {}
        for s in service.spines:
            intlinks[s.device] = {}
            for l in s.connections:
                key = '{}->{}'.format(s.device, l.leaf)
                inet = getintnet(root, service, username, key)
                intlinks[s.device][l.leaf] = inet
                self.log.info('Int link {} -> {}: {}'.format(s.device,l.leaf, inet))
        return intlinks

    # Generate the /vxlan-spine instances
    def generate_spines(self, service, globalpim, pimips, loopbackips, intlinks):
        # Try generating every spine
        for s in service.spines:
            vars = ncs.template.Variables()
            template = ncs.template.Template(service)
            vars.add('SPINE', s.device)
            # Base config
            try:
                vars.add('PIM_IP', get_ip(globalpim))
                vars.add('LOOPBACK0', get_ip(loopbackips[s.device]))
                vars.add('LOOPBACK1', get_ip(globalpim))
                template.apply('vxlan-spine-create', vars)

            except Exception as e:
                self.log.warning('Spine creation failed for {}, beacuse {}.'.format(s.device, e))

            # List all spines as neighbors
            for se in service.spines:
                vars.add('OTHER_SPINE', se.device)
                if loopbackips[se.device] is None:
                    continue
                vars.add('OTHER_ROUTERID', get_ip(loopbackips[se.device]))
                template.apply('vxlan-spine-create-spine', vars)

            # Add in leaf-links
            for l in s.connections:
                vars.add('LEAF', l.leaf)
                vars.add('IF', l.interface)
                if loopbackips[l.leaf] is None:
                  continue
                vars.add('LEAF_ROUTERID', get_ip(loopbackips[l.leaf]))
                net = intlinks[s.device][l.leaf]
                if net is None:
                  continue
                net = ipaddress.ip_network(unicode(net))
                hosts = list(net.hosts())
                vars.add('MY_IP', '{}/{}'.format(hosts[0],net.prefixlen))
                template.apply('vxlan-spine-create-links', vars)


    # Generate the /vxlan-leaf instances
    def generate_leaves(self, service, globalpim, pimips, loopbackips, intlinks):
        # Try generating every spine
        for l in service.leaves:
            vars = ncs.template.Variables()
            template = ncs.template.Template(service)
            vars.add('LEAF', l.device)
            # Base config
            try:
                vars.add('PIM_IP', get_ip(globalpim))
                vars.add('LOOPBACK0', get_ip(loopbackips[l.device]))
                vars.add('LOOPBACK1', get_ip(pimips[l.device]))
                template.apply('vxlan-leaf-create', vars)

            except Exception as e:
                self.log.warning('Leaf creation failed for {}, beacuse {}.'.format(s.device, e))


            # Add in spine-links
            for s in l.connections:
                vars.add('SPINE', s.spine)
                vars.add('IF', s.interface)
                if loopbackips[s.spine] is None:
                  continue
                vars.add('SPINE_ROUTERID', get_ip(loopbackips[s.spine]))
                net = intlinks[s.spine][l.device]
                if net is None:
                  continue
                net = ipaddress.ip_network(unicode(net))
                hosts = list(net.hosts())
                vars.add('MY_IP', '{}/{}'.format(hosts[1],net.prefixlen))
                template.apply('vxlan-leaf-create-links', vars)

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        (globalpim, pimips) = self.allocate_pim(root, service, tctx.username)
        self.log.info('PIM IPs: {}'.format(pimips))

        loopbackips = self.allocate_loopbacks(root, service, tctx.username)
        self.log.info('Loopback IPs: {}'.format(loopbackips))

        intlinks = self.allocate_interior(root, service, tctx.username)
        self.log.info('Internal nets: {}'.format(intlinks))

        create_vni_pool(service)
        create_vlan_pool(service)

        # No point in proceeding until at least some allocation is done
        if globalpim is None:
            self.log.warning('PIM not yet allocated')
            return
        self.log.info('Global PIM: {}'.format(globalpim))

        self.generate_spines(service, globalpim, pimips, loopbackips, intlinks)

        self.generate_leaves(service, globalpim, pimips, loopbackips, intlinks)
