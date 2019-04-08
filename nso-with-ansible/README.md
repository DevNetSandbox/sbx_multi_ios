
<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Introduction to Network Services Orchestrated (NSO) with Ansible](#introduction-to-network-services-orchestrated-nso-with-ansible)
- [Topology](#topology)
- [Pre-reqs](#pre-reqs)
- [Lab Setup (~10 min)](#lab-setup-10-min)
- [Ansible Walkthrough](#ansible-walkthrough)
	- [Inventory](#inventory)
		- [Device Groups](#device-groups)
	- [Device Operations](#device-operations)
	- [Playbooks](#playbooks)
		- [NTP Configuration](#ntp-configuration)
- [](#)
- [NSO Walkthrough](#nso-walkthrough)
	- [Importing devices into NSO](#importing-devices-into-nso)
	- [Device Groups](#device-groups)
	- [Device Operations](#device-operations)
	- [Device Templates](#device-templates)
		- [Creating Templates](#creating-templates)
		- [Compliance Reporting](#compliance-reporting)
		- [Applying Templates](#applying-templates)
		- [Transactions, Rollbacks](#transactions-rollbacks)
- [NSO with Ansible Walkthrough](#nso-with-ansible-walkthrough)
- [TODO](#todo)

<!-- /TOC -->
# Introduction to Network Services Orchestrated (NSO) with Ansible


# Topology

we will be using the [virlfiles/xe-xr-nx](https://github.com/virlfiles/xe-xr-nx) topology

# Pre-reqs

* VPN connection to an active devnet sbx_multi_ios reservation



# Lab Setup (~10 min)

  * **Note:** all steps completed from the devbox (TODO: do we need local?)


  1. ssh to devbox `ssh developer@10.10.20.20`

  2. Clone required code

  ```
  git clone https://github.com/DevNetSandbox/sbx_multi_ios
  cd sbx_multi_ios/nso-with-ansible
  ```

  3. Install Dependencies

  ```
  python3.6 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

  4. Launch demo environment

  ```
  make test
  ```

  This step will take a few minutes while we get things setup.
  You should see output similar to the following:

  ```
  [developer@devbox nso-with-ansible]$make test
  Stopping All Netsim Instances...
  confd: no process found
  make: [clean-netsim] Error 1 (ignored)
  rm: cannot remove ‘README.netsim’: No such file or directory
  make: [clean-netsim] Error 1 (ignored)
  Stopping NSO...
  connection refused (stop)
  make: [clean-nso] Error 1 (ignored)
  ncsc -c packages/pipe-yaml/yaml-c.cli -o packages/yaml-c.ccl
  ncs-setup --dest . --package cisco-ios --package cisco-iosxr --package cisco-nx
  export PATH=$PATH:packages/pipe-yaml; echo $PATH; ncs
  /opt/nso/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/developer/bin:packages/pipe-yaml
  Creating default environment from topology.virl
  Localizing {{ gateway }} with: 172.16.30.254
  Localizing rsa modulus 768 with: rsa modulus 1024
  Waiting 10 minutes for nodes to come online....
    [####################################]  100%
  virl generate nso --syncfrom
  Updating NSO....
  Successfully added VIRL devices to NSO

      NSO Sync Report

  ╒══════════╤══════════╕
  │ Device   │ Result   │
  ╞══════════╪══════════╡
  │ nx       │ SUCCESS  │
  ├──────────┼──────────┤
  │ xe       │ SUCCESS  │
  ├──────────┼──────────┤
  │ xr       │ SUCCESS  │
  ╘══════════╧══════════╛
  ```

At this point we have a running VIRL simulation, NSO installed and running, and we're ready to get started.

# Ansible Walkthrough

## Inventory

Ansible works against multiple systems in your infrastructure at the same time. It does this by selecting portions of systems listed in Ansible’s inventory, which defaults to being saved in the location /etc/ansible/hosts. You can specify a different inventory file using the -i <path> option on the command line.

Not only is this inventory configurable, but you can also use multiple inventory files at the same time and pull inventory from dynamic services (like NSO) or different file formats (YAML, ini, etc)

For detailed information on Ansible Inventory see [here](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)

For our purposes we will use `virlutils` to generate an inventory suitable for our running simulation.

```
virl generate ansible
```

### Device Groups

## Device Operations

Ansible uses modules to configure devices, these modules allow various operational/configuration commands to be running.  In the following example we will use the [./ansible_playbooks](./ansible_playbooks/enable_ssh.yaml) playbook to enable SSH on the device `xr`
```
cd ansible_playbooks
ansible-playbook -i default_inventory.yaml enable_ssh.yaml

```
## Playbooks

```
cd ansible_playbooks
ansible-playbook -i default_inventory.yaml configure_ntp.yaml
```

### NTP Configuration

#


# NSO Walkthrough


We will start out by using the CLI of NSO.  The CLI provides a great starting point for Network Engineers who are very comfortable with "c-style" or "j-style" command line interfaces.  This CLI represents all of the devices under management with a consistent CLI, while still providing all of the benefits of NSO in terms of transactions, rollbacks, it also provides some handy utilities for generating API payloads as you look to integrate in with other workflows.

To the NSO CLI can be accessed via the following command from the NSO server (devbox)

```
ncs_cli -u admin
```

## Importing devices into NSO

During the initial setup, the VIRL devices were  imported into NSO.  In doing so, we've already introduced you to one of the features of NSO, which is it's northbound REST API, but we will get to that in a second.

NSO maintains a configuration database (CDB) of all the devices and services that it manages. The CDB is a YANG based datastore, and is the source of truth for all things NSO(including NSO itself)  Devices can be added to NSO in a variety of ways outline below.  You can skip this section and proceed to.

1. Using the NSO CLI
2. Using NSO REST API - this approach is useful for integrating NSO into other tools, such
as CMDB/ITSM.

3. Using an Ansible Playbook - Ansible can also consume the nortbound API provided by
NSO to perform operations.


**Add Network Devices using the NSO CLI**

This approach involves using the NSO CLI, this approach should be intuitive
for those familiar with network device CLI's

A device can be entered directly into the CLI as shown in the example below

**IMPORTANT NOTE:** IP's are assigned dynamically to the VIRL nodes,
so you need to double check these examples shown below to make sure you are using the correct IP address.  The VIRL nodes can be viewed using the `virl nodes` command.

```
admin@ncs# config t
Entering configuration mode terminal
admin@ncs(config)# devices device xe
admin@ncs(config-device-xe)# address 172.16.30.61
admin@ncs(config-device-xe)# authgroup virl
admin@ncs(config-device-xe)# device-type cli ned-id cisco-ios
admin@ncs(config-device-xe)# device-type cli protocol telnet
admin@ncs(config-device-xe)# state admin-state unlocked
```

The changes made in configuration mode do not take effect immediately, instead they must be `committed` to the configuration database. Prior to committing you have a chance to preview **all** of the configuration changes that are staged for commit by performing a `commit dry-run`

```
admin@ncs(config-device-xe)# commit dry-run
cli {
    local-node {
        data  devices {
             +    device xe {
             +        address 172.16.30.61;
             +        authgroup virl;
             +        device-type {
             +            cli {
             +                ned-id cisco-ios;
             +                protocol telnet;
             +            }
             +        }
             +        state {
             +            admin-state unlocked;
             +        }
             +    }
              }
    }
}
```

Once the commit happens, the **changes are atomic** which means that all of the changes will be made to any/all devices, or no change is made.


In addition to manually entering these CLI commands can be stored in an external script file, and `load merged` into the configuration of NSO.
We will use the files located in the  [nso_cli_scripts](./nso_cli_scripts) directory to set some things up and save you some keystrokes.

## Device Groups

Device groups are useful for managing a large number of devices, membership in groups can be organized in any number of ways; location, role, type, etc.

Some important notes about device groups.
* A device can be a member of multiple groups.
* Groups can contain other groups

The [nso_cli_scripts/create_device_groups.cli](./nso_cli_scripts/create_device_groups.cli) script creates a groups `routers`, `switches`, and `all`

```
admin@ncs# config t
Entering configuration mode terminal
admin@ncs(config)# load merge nso_cli_scripts/create_device_groups.cli
Loading.
53 bytes parsed in 0.12 sec (423 bytes/sec)
admin@ncs(config-device-group-all)# commit dry-run
cli {
    local-node {
        data  devices {
             +    device-group all {
             +        device-group [ routers switches ];
             +    }
             +    device-group routers {
             +        device-name [ xe xr ];
             +    }
             +    device-group switches {
             +        device-name [ nx ];
             +    }
              }
    }
}
admin@ncs(config)# commit
```

The configuration can also be reviewed by running the following command.

```
admin@ncs# show running-config devices device-group
devices device-group all
 device-group [ routers switches ]
!
devices device-group routers
 device-name [ xe xr ]
!
devices device-group switches
 device-name [ nx ]
!
```

Or converted into structured data via the CLI, this is especially useful for generating API payloads

As XML
```
<config xmlns="http://tail-f.com/ns/config/1.0">
  <devices xmlns="http://tail-f.com/ns/ncs">
  <device-group>
    <name>all</name>
    <device-group>routers</device-group>
    <device-group>switches</device-group>
  </device-group>
  <device-group>
    <name>routers</name>
    <device-name>xe</device-name>
    <device-name>xr</device-name>
  </device-group>
  <device-group>
    <name>switches</name>
    <device-name>nx</device-name>
  </device-group>
  </devices>
</config>
```

As JSON
```
admin@ncs# show running-config devices device-group | display json
{
  "data": {
    "tailf-ncs:devices": {
      "device-group": [
        {
          "name": "all",
          "device-group": ["routers", "switches"]
        },
        {
          "name": "routers",
          "device-name": ["xe", "xr"]
        },
        {
          "name": "switches",
          "device-name": ["nx"]
        }
      ]
    }
  }
}
```

You can even generate your own `pipeCmds` as demonstrated using the [pipe-yaml](./pipe-yaml) package that's included in this repo.

This is super useful when integrating with Ansible!

```
admin@ncs# show running-config devices device-group | display json | yaml
data:
  tailf-ncs:devices:
    device-group:
    - device-group: [routers, switches]
      name: all
    - device-name: [xe, xr]
      name: routers
    - device-name: [nx]
      name: switches
```
## Device Operations

NSO supports several important operations for reconciling the configuration present in the configuration database (CDB), and the configuration present on the devices. These operations can be applied to all devices, a particular device-group, or a single device.

**check-sync** - performs a quick check as to whether the device configuration is consistent with the configuration database.

**compare-config** - allows you to review the differences in the event that a device is out of sync.

**sync-from** - bring the configuration database into a consistent state with the device

**sync-to** - bring the device into a consistent state with the configuration database

As with configuration these operations can be triggered via CLI or API.

via CLI
```
admin@ncs# devices device-group all sync-from
sync-result {
    device nx
    result true
}
sync-result {
    device xe
    result true
}
sync-result {
    device xr
    result true
}
```

or via API

```
curl -X POST -u admin:admin http://localhost:8080/api/running/devices/device-group/all/_operations/sync-from
```

**IMPORTANT NOTE**: notice the consistency between the CLI operation and the API.  This is because both of them are merely representations of the configuration stored in the CDB.

## Device Templates

Device templates represent a desired configuration for devices being managed by NSO.  They can be used across multiple device types, and compliance reports can be generated with any deviations

The following steps will load some device configuration templates.

### Creating Templates

Apply the [nso_templates/standard_ntp_template.xml](./nso_templates/standard_ntp_template.xml) file via load merge.

Each template node e.g `ntp` can contain a list of configuration for each device-type (NED) that which NSO manages.  When templates are applied, NSO automatically handles the logic of applying the appropriate configuration based on the device type. Additionally, `tags` can be added to templates. A tag is inherited to its sub-nodes until a new tag is introduced.

* **merge** with a node if it exists, otherwise create the node. This is the default operation if no operation is explicitly set.

* **replace**: configuration within this node on the target device which is not in the template will be automatically removed.

* **create**: only apply the configuration if no other configuration of this node applied to the device.

* **nocreate**: Only apply the configuration if this node already exists on the device.

These template files can be easily created based off existing devices using the conversion mechanisms outlined earlier. e.g `show running-config devices device nx config nx:ntp | display xml`

```
admin@ncs(config)# load merge nso_templates/standard_ntp_template.xml
Loading.
1.13 KiB parsed in 0.04 sec (25.22 KiB/sec)
admin@ncs(config)# commit
```

### Compliance Reporting

Compliance Reports can be created to audit device configurations against the template contents. These reports can executed via CLI, or API and the results can be output in text, XML, or HTML formats. For convenience these reports are also hosted on the NSO web server so that they can be linked to from other systems.

```
admin@ncs(config)# compliance reports report ntp_audit compare-template standard_ntp all
admin@ncs(config-compare-template-standard_ntp/all)# commit
Commit complete.
```

```
admin@ncs# compliance reports report ntp_audit run outformat html
id 2
compliance-status violations
info Checking 3 devices and no services
location http://localhost:8080/compliance-reports/report_2_admin_1_2019-4-4T23:54:29:0.html
```

You can use the provided URL to access the report.

**NOTE:** you may need to change localhost to 10.10.20.20 to view this URL

### Applying Templates

Templates can applied via CLI or API.

```
admin@ncs(config)# devices device-group all apply-template template-name standard_ntp
apply-template-result {
    device nx
    result ok
}
apply-template-result {
    device xe
    result ok
}
apply-template-result {
    device xr
    result ok
}
admin@ncs(config)# commit dry-run

<any required changes as computed by NSO will be displayed here>

admin@ncs(config)#
admin@ncs(config)# commit

```

### Transactions, Rollbacks

As was mentioned earlier, everything in NSO is a transaction, and in addition to being `atomic` They also give the ability `rollback` any configuration that was changed during that transaction.


```
admin@ncs(config)# rollback configuration
admin@ncs(config)# commit dry-run

< automatically generated backout configuration >

admin@ncs(config)#
```

After loading the rollback configuration, another commit (which could subsequently be rolled back as well) is performed.

# NSO with Ansible Walkthrough

As highlighted earlier, NSO provides nortbound API's for use with integrating with other tools and systems.  Integrating NSO with Ansible can become a force multiplier in cross-domain orchestration.

* Playbooks can be decoupled from low level device modules, and instead use common modules across all device types, which can interact with the CDB, or provide other operations.
* Ansible can take advantage of the transaction/rollback capabilities of NSO.
* Ansible can provide workflow to multi step operations.
* NSO can compute required changes on the fly and provide compliance reporting.


```
cd ansible_playbooks
ansible-playbook sync_from_devices.yaml
(venv) [developer@devbox ansible_playbooks]$ansible-playbook sync_from_devices.yaml

PLAY [Synchronization of Devices] ************************************************************************************

TASK [NSO sync-from action] ******************************************************************************************
changed: [localhost]

PLAY RECAP ***********************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0
```




# TODO

- [x] Topology
- [ ] setup docs/scripts
- [ ] Ansible Playbook
- [ ] "bonus material"
- [ ] Lab Guide
- [ ] Slides
