import ncs
import resource_manager.ipaddress_allocator as ip_allocator
import resource_manager.id_allocator as id_allocator

def getpimpool(service):
    return '{}-pim-pool'.format(service.name)

def getlooppool(service):
    return '{}-loopback-pool'.format(service.name)

def getintpool(service):
    return '{}-interior-pool'.format(service.name)

def getvnipool(fabric):
    return '{}-vni-pool'.format(fabric)

def getvlanpool(fabric):
    return '{}-vlan-pool'.format(fabric)


def getpimip(root, service, username, alloc_name):
    poolname = getpimpool(service)
    ip_allocator.net_request(service,
                             "/vxlan-fabric:vxlan-fabric[name='{}']".format(service.name),
                             username,
                             poolname,
                             alloc_name,
                             32)
    ip = ip_allocator.net_read(username, root,
                               poolname,
                               alloc_name)
    return ip

def getloopip(root, service, username, alloc_name):
    poolname = getlooppool(service)
    ip_allocator.net_request(service,
                             "/vxlan-fabric:vxlan-fabric[name='{}']".format(service.name),
                             username,
                             poolname,
                             alloc_name,
                             32)
    ip = ip_allocator.net_read(username, root,
                               poolname,
                               alloc_name)
    return ip

def getintnet(root, service, username, alloc_name):
    poolname = getintpool(service)
    ip_allocator.net_request(service,
                             "/vxlan-fabric:vxlan-fabric[name='{}']".format(service.name),
                             username,
                             poolname,
                             alloc_name,
                             30)
    ip = ip_allocator.net_read(username, root,
                               poolname,
                               alloc_name)
    return ip

def create_vni_pool(service):
    vars = ncs.template.Variables()
    vars.add('POOL_NAME', getvnipool(service.name))
    vars.add('START', 10000)
    vars.add('END', 20000)
    template = ncs.template.Template(service)
    template.apply('vxlan-id-pool-create', vars)


def getvniid(root, service, servicepath, username, fabric, alloc_name):
    poolname = getvnipool(fabric)
    id_allocator.id_request(service,
                           servicepath,
                           username,
                           poolname,
                           alloc_name,
                           False)
    vniid = id_allocator.id_read(username, root,
                                 poolname,
                                 alloc_name)

    return vniid

def getvlanid(root, service, servicepath, username, fabric, alloc_name):
    poolname = getvlanpool(fabric)
    id_allocator.id_request(service,
                           servicepath,
                           username,
                           poolname,
                           alloc_name,
                           False)
    vlanid = id_allocator.id_read(username, root,
                                 poolname,
                                 alloc_name)

    return vlanid

def create_vlan_pool(service):
    vars = ncs.template.Variables()
    vars.add('POOL_NAME', getvlanpool(service.name))
    vars.add('START', 10)
    vars.add('END', 4000)
    template = ncs.template.Template(service)
    template.apply('vxlan-id-pool-create', vars)
