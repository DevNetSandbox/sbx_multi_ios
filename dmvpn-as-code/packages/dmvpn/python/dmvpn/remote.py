import ncs
import ipaddress


def remote_configuration(service, tunnel_ips, lan_networks, logger):

    for remote in service.remotes:
        logger.info("Configuring {}".format(remote.device))
        tunnel_ip = tunnel_ips[remote.device]
        lan_net = lan_networks[remote.device]
        vars = ncs.template.Variables()

        # bail if we havent got an allocation yet
        template = ncs.template.Template(service)
        if tunnel_ip is None:
            continue

        if lan_net is None:
            continue

        # compute some required properties
        source_interface = remote.public_interface.type + \
            remote.public_interface.number

        net = ipaddress.IPv4Network(lan_net)
        # usable host ips
        hosts = list(net.hosts())
        # remote uses the first usable IP of the network
        lan_ip = hosts[0]
        lan_network = net.network_address
        lan_mask = net.netmask
        lan_wildcard_mask = net.hostmask

        primary_headend_public_ip = tunnel_ips['primary_headend_public_ip']
        primary_headend_tunnel_ip = tunnel_ips['primary_headend_tunnel_ip']

        # setup template vars
        vars.add('DEVICE', remote.device)
        vars.add('IS_REMOTE', 'true')
        vars.add('PSK', service.psk)
        vars.add('TUNNEL_NUMBER', service.tunnel_number)
        vars.add('TUNNEL_IF_DESCRIPTION', service.name)
        vars.add('TUNNEL_IP', tunnel_ip.ip)
        vars.add('TUNNEL_MASK', tunnel_ip.netmask)
        vars.add('TUNNEL_NETWORK', tunnel_ip.network.network_address)
        vars.add('TUNNEL_WILDCARD_MASK', tunnel_ip.network.hostmask)
        vars.add('SOURCE_INTERFACE', source_interface)
        vars.add('PRIMARY_HEADEND_PUBLIC_IP', primary_headend_public_ip)
        vars.add('PRIMARY_HEADEND_TUNNEL_IP', primary_headend_tunnel_ip)
        vars.add('LAN_NETWORK', lan_network)
        vars.add('LAN_MASK', lan_mask)
        vars.add('LAN_WILDCARD_MASK', lan_wildcard_mask)
        vars.add('LAN_IP', lan_ip)
        logger.info("Remote: {} Vars: {}".format(remote.device, vars))

        try:
            template.apply('common-crypto-config', vars)
            template.apply('remote-lan-interface', vars)
            template.apply('eigrp-template', vars)
            template.apply('remote-tunnel-interface', vars)
            template.apply('remote-dhcp-pool', vars)
        except Exception as e:
            msg = 'Remote configuration failed for {}, beacuse {}'
            logger.warning(msg.format(remote.device, e))
