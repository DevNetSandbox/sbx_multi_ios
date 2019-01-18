import ncs
from ncs.application import Service

class LeafService(Service):
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        vars.add('HOSTNAME', service.name)
        vars.add('GROUP_RANGE', service.group_range)
        vars.add('SSM_LIST', service.ssm_list)
        vars.add('AS_NUMBER', service.as_number)
        vars.add('PIM_IP', service.pim_ip)

        vars.add('LOOPBACK0_IP', service.loopback0)
        vars.add('LOOPBACK1_IP', service.loopback1)

        self.log.info('Vars', vars)
        template = ncs.template.Template(service)
        template.apply('vxlan-evpn-base', vars)
        template.apply('vxlan-evpn-leaf', vars)
