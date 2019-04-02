"""
Main logic for provisioning headend router in DMVPN
"""
import ncs


def headend_configuration(service, tunnel_ips, logger):
    tunnel_ip = tunnel_ips[service.primary_headend.device]
    vars = ncs.template.Variables()
    template = ncs.template.Template(service)

    # bail if we dont have an IP allocated yet
    if tunnel_ips[service.primary_headend.device] is None:
        return

    source_interface = service.primary_headend.public_interface.type + \
        service.primary_headend.public_interface.number

    vars.add('DEVICE', service.primary_headend.device)
    vars.add('IS_REMOTE', False)
    vars.add('LAN_NETWORK', False)
    vars.add('LAN_WILDCARD_MASK', False)
    vars.add('TUNNEL_NUMBER', service.tunnel_number)
    vars.add('TUNNEL_IF_DESCRIPTION', service.name)
    vars.add('PSK', service.psk)
    vars.add('TUNNEL_IP', tunnel_ip.ip)
    vars.add('TUNNEL_MASK', tunnel_ip.netmask)
    vars.add('TUNNEL_NETWORK', tunnel_ip.network.network_address)
    vars.add('TUNNEL_WILDCARD_MASK', tunnel_ip.network.hostmask)
    vars.add('SOURCE_INTERFACE', source_interface)
    logger.info("Generating Headend configuration with: ".format(vars))
    try:
        template.apply('common-crypto-config', vars)
        template.apply('eigrp-template', vars)
        template.apply('headend-tunnel-interface', vars)
    except Exception as e:
        msg = 'Headend configuration failed for {}, beacuse {}'
        logger.warning(msg.format(service.primary_headend.device, e))
