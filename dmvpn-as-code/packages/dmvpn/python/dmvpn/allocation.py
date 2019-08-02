import ncs
import resource_manager.ipaddress_allocator as ip_allocator
from .lookups import get_public_ip
import ipaddress


def allocate_lan_networks(root, service, username, logger):
    """ Main logic for allocating lan networks for remote sites"""

    lan_pool = service.lan_pool  # 10.16.0.0/16
    pool_name = get_lan_pool_name(service)
    prefix = lan_pool.split('/')[0]  # 10.16.0.0
    prefix_len = lan_pool.split('/')[1]  # 16

    vars = ncs.template.Variables()
    vars.add('POOL_NAME', pool_name)
    vars.add('PREFIX', prefix)
    vars.add('PREFIX_LEN', prefix_len)
    template = ncs.template.Template(service)
    template.apply('create-ip-pool', vars)

    lan_networks = {}
    for r in service.remotes:
        lan_networks[r.device] = None
        logger.info("Allocating LAN network for {}".format(r.device))
        lan_net = get_lan_network(root,
                                  service,
                                  username,
                                  r.device)
        if not(lan_net is None):
            lan_networks[r.device] = lan_net

    return lan_networks


def allocate_tunnel_ips(root, service, username, logger):
    """ creates a pool from which we allocate tunnel IPs for all members"""
    # create an IP pool for the provided network.
    tunnel_pool = service.tunnel_pool  # 10.16.8.0/24
    pool_name = get_tunnel_pool_name(service)
    prefix = tunnel_pool.split('/')[0]  # 10.16.8.0
    prefix_len = tunnel_pool.split('/')[1]  # 24
    vars = ncs.template.Variables()
    vars.add('POOL_NAME', pool_name)
    vars.add('PREFIX', prefix)
    vars.add('PREFIX_LEN', prefix_len)
    template = ncs.template.Template(service)
    template.apply('create-ip-pool', vars)

    # request a reservation from that pool for each member
    tunnel_interface_ips = {}

    # lookup the primary hubs public ip
    devs = root.devices.device
    primary_headend = service.primary_headend.device
    public_interface_type = service.primary_headend.public_interface.type
    public_interface_num = service.primary_headend.public_interface.number

    headend_public_ip = get_public_ip(devs,
                                      primary_headend,
                                      public_interface_type,
                                      public_interface_num)

    tunnel_interface_ips['primary_headend_public_ip'] = headend_public_ip

    # Allocate the first address to the headend
    # the allocation may not be completed yet, we can test for it later
    tunnel_interface_ips[primary_headend] = None

    primary_ip = get_tunnel_ip(root,
                               service,
                               username,
                               primary_headend)

    # wait the allocation is complete
    if primary_ip:
        primary_ip = get_ip_object(primary_ip, prefix_len)
        # update the dict
        tunnel_interface_ips[primary_headend] = primary_ip
        tunnel_interface_ips['primary_headend_tunnel_ip'] = primary_ip.ip
        logger.info("Allocated {} for {}".format(primary_ip,
                                                 primary_headend))
    else:
        logger.error("Failed to allocate IP for primay headend")

    # then all remotes
    for r in service.remotes:
        tunnel_interface_ips[r.device] = None
        tunnel_ip = get_tunnel_ip(root,
                                  service,
                                  username,
                                  r.device)
        if not(tunnel_ip is None):
            tunnel_ip = get_ip_object(tunnel_ip, prefix_len)
            tunnel_interface_ips[r.device] = tunnel_ip
    return tunnel_interface_ips


# define naming standards for some things
def get_lan_pool_name(service):
    return '{}-lan-pool'.format(service.name)


def get_tunnel_pool_name(service):
    return '{}-tunnel-pool'.format(service.name)


def get_lan_ip(lan_net):
    """returns first host address given an allocated lan network"""
    ip_network = ipaddress.ip_network(lan_net)
    first = next(ip_network.hosts())
    return first


def get_ip_object(ip, prefix_len):
    """
    fix ip reservation (/32) back to the original prefix_len
    from the pool.  also converts to IPV4Interace object

    """
    ip_mask = ip.split('/')[0] + "/" + prefix_len
    # now we convert to an IPInterface, this will be helpful later
    ip_obj = ipaddress.IPv4Interface(ip_mask)
    return ip_obj


def get_tunnel_ip(root, service, username, alloc_name):

    poolname = get_tunnel_pool_name(service)
    # reserve an IP
    ip_allocator.net_request(service,
                             "/dmvpn:dmvpn[name='{}']".format(service.name),
                             username,
                             poolname,
                             alloc_name,
                             32)
    ip = ip_allocator.net_read(username, root,
                               poolname,
                               alloc_name)

    return ip


def get_lan_network(root, service, username, alloc_name):

    poolname = get_lan_pool_name(service)
    # reserve an IP
    ip_allocator.net_request(service,
                             "/dmvpn:dmvpn[name='{}']".format(service.name),
                             username,
                             poolname,
                             alloc_name,
                             29)
    ip = ip_allocator.net_read(username, root,
                               poolname,
                               alloc_name)
    return ip
