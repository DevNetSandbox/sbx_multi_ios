# helpers to quickly gather information out of the configuration
# database, other sources can be used as well.


def get_public_ip(devs, devname, interface_name, interface_number):
    """
    quick helper for getting a devices public interface address
    """
    type = devs[devname].device_type.cli.ned_id.split(':')[-1]
    ip = None
    # only ios is supported currently
    if type == 'cisco-ios':
        type = getattr(devs[devname].config.ios__interface, interface_name)
        public_interface = type[interface_number]
        ip = public_interface.ip.address.primary.address

    if ip:
        return ip
    else:
        msg = "{} not implemented by this package"
        raise NotImplementedError(msg.format(type))
