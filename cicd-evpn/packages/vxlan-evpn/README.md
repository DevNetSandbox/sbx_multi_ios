# VXLAN-EVPN Function pack

This is a function pack that implements VXLAN-EVPN functionality. It supports multiple fabrics and multiple tenants in each fabric.

## Building

### Local or remote files

This project uses `ncs-project` to fetch data from git. If you are not a member of the NSO core team you will need the `cisco-nx` NED and the `resource-manager` package in tar-balls on the local filesystem. In this case start with
```
cp project-meta-data-local.xml project-meta-data.xml
```

### Building

Clean up and then build everything with
```
make reset
make clean
make all
```

## Running NETSIM

Reset the environment and start a clean one:
```
ncs-setup --dest .
make netsim
make start
```

This starts a netsim environment with 4 spine nodes and 2 leaf nodes.

## Running VIRL

Pretty much the same, only, don't do `make netsim` and do the VIRL stuff instead.


## Example configs

Here is an example fabric (`example/fabric-c.cli`) that works with the netsim environment (don't forget `autowizard false` before entering config mode!)

```
vxlan-fabric fabric1
 pim-pool      100.2.1.0/24
 loopback-pool 10.2.1.0/24
 interior-pool 172.16.0.0/16
 spines spine0
  connections leaf0
   interface 1/1
  !
  connections leaf1
   interface 1/2
  !
  connections leaf2
   interface 1/3
  !
  connections leaf3
   interface 1/4
  !
 !
 spines spine1
  connections leaf0
   interface 1/1
  !
  connections leaf1
   interface 1/2
  !
  connections leaf2
   interface 1/3
  !
  connections leaf3
   interface 1/4
  !
 !
 leaves leaf0
  connections spine0
   interface 1/1
  !
  connections spine1
   interface 1/2
  !
 !
 leaves leaf1
  connections spine0
   interface 1/1
  !
  connections spine1
   interface 1/2
  !
 !
 leaves leaf2
  connections spine0
   interface 1/1
  !
  connections spine1
   interface 1/2
  !
 !
 leaves leaf3
  connections spine0
   interface 1/1
  !
  connections spine1
   interface 1/2
  !
 !
!
```

Here is an example tenant (`example/tenant1-c.cli`):
```
vxlan-tenant Tenant-1
 fabric fabric1
 segments Seg1
  network      10.0.11.0/24
  suppress-arp false
  connection leaf1 1/3
  connection leaf1 1/4
 !
 segments Seg2
  network      10.0.12.0/24
  suppress-arp false
  connection leaf1 1/3
 !
!
```
