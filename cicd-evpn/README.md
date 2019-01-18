# cicd-evpn

A multi-fabric VXLAN EVPN Infrastructure as Code Proof of Concept.

This repository is a code base which implements a full CI/CD pipeline for network configuration, as well as offering a basic service catalog of playbooks which
can be offered via Tower/AWX, executed directly from
other workflows, or ran manually.

# Technology Stack

* Ansible (2.5 or later)
* NSO (4.6 or later)
* Netsim (for providing local dev enviroments)
* Cisco VIRL (for testing "live" deployments)
* pyATS for running acceptance tests after a deployment
* AWX (optional for service-catalog type use cases)

# NSO Service Details

The following service models are defined in (./packages/vxlan-evpn)
  * vxlan-leaf
  * vxlan-spine
  * vxlan-fabric
  * vxlan-tenant

# Topology

The [./topology.virl](topology.virl) file provides a spine-leaf topology for use with Cisco VIRL

![Alt Text](https://github.com/virlfiles/spine-leaf/raw/master/topology.png)


# Catalog

Several ad-hoc services are located in the [./catalog](./catalog) directory.  These scripts are useful for ad-hoc jobs, or offered via AWX/Tower Templates

### new_tenant.yaml

Creates a new VXLAN EVPN tenant for in a given fabric

### Usage


```
ansible-playbook -i inventory/dev.yaml \
  -e tenant_name=foo \
  -e network_cidr="10.10.0.0/24" \
  -e segment_name=seg1 \
  -e suppress_arp="false" \
  catalog/new_tenant.yaml
```
