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


# Topology
