# HEMP

This is a proof of concept VPN **H**ead **E**nd **M**anagement **P**latform.



It is designed to be basic demonstration of a VPN service package for Cisco Network Services Orchestrator (NSO) as well as an example of integrating NSO with custom portals using it's northbound API interfaces.

### Pre-Requisites

This code is designed to be ran in the [Multi-IOS Cisco Test Network Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology)


## Setup

##### VPN into Sandbox

VPN credentials and gateways are emailed to you once your sandbox is ready.

##### Connect to Devbox
While VPN'd into the sandbox. SSH into the  devbox

```
ssh developer@10.10.20.20
```
The
default credentials are `developer/C1sco12345`

##### Clone the repository
```
git clone https://github.com/DevNetSandbox/sbx_multi_ios.git
cd sbx_multi_ios/hemp
```

##### Run Setup script

This following script should cover all the initial installation

```
./setup.sh
```

Once the process is complete, HEMP should be accessible at http://10.10.20.20:5001


The topology contains two routers `partner3` and `partner4`  these devices are preconfigured to connect to the headend, you can use the management portal to configure the headends appropriately.

* `partner1` and `partner2` have been preconfigured using Ansible and associated NSO modules to configure the corresponding headend configuration
* `partner3` and `partner4` are preconfigured on the partner side but can be added on the headends via the management portal given the following parameters.

  ```
  partner3:
    - partner_name: partner3
      device:
        - headend
      sequence: 103
      peer_ip: 172.16.252.3
      isakmp_algo: 3des
      isakmp_group: 2
      pre_shared_key: cisco
      transform_encryption: esp-3des
      transform_auth: esp-md5-hmac
      acl_number: "101"
      acl_rule: "permit ip 192.168.0.0 0.0.0.255 192.168.3.0 0.0.0.255"

  partner4:
    - partner_name: partner4
      device:
        - headend
      sequence: 104
      peer_ip: 172.16.252.4
      isakmp_algo: 3des
      isakmp_group: 2
      pre_shared_key: cisco
      transform_encryption: esp-3des
      transform_auth: esp-md5-hmac
      acl_number: "104"
      acl_rule: "permit ip 192.168.0.0 0.0.0.255 192.168.4.0 0.0.0.255"

  ```
