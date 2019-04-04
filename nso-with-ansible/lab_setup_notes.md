# Introduction to Network Services Orchestrated (NSO) with Ansible

# Topology

we will be using the [virlfiles/xe-xr-nx](https://github.com/virlfiles/xe-xr-nx) topologys

# Pre-reqs

* devnet sbx_multi_ios reservation


# Overall Lab Flow (~90 minutes)

## Lab Logistics / Setup Review (~10min)
## Lab Setup (~10 min)

  * **Note:** all steps completed from the devbox (TODO: do we need local?)

  * details
    1. ssh to devbox `ssh developer@10.10.20.20`
    2. clone repo `git clone https://github.com/DevNetSandbox/sbx_multi_ios`
    3. launch topology

      ```
      cd sbx_multi_ios/nso-with-ansible
      virl up virlfiles/xe-xr-nx --provision
      ```
    4. initialize/start NSO
      ```
      ncs-setup --dest . --package cisco-ios --package cisco-iosxr --package cisco-nx
      ncs
      ```      
    5. install python dependencies
      ```
      python3.6 -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      ```

## Importing a device into NSO

We will add the three devices in our topology, using three different approaches
to highlight the different options that you have available to you.

1. Manual - this approach involves using the NSO CLI, this approach should be intuitive
for those familiar with network device CLI's

2. Using NSO REST API - this approach is useful for integrating NSO into other tools, such
as CMDB/ITSM.

3. Using an Ansible Playbook - Ansible can also consume the nortbound API provided by
NSO to perform operations.


## Device Groups

1. Create device group for all devices

## Configuration Templates / Compliance

1. create configuration template
2. create compliance report

It should take about 6-7 minutes to boot up these nodes, we can review slides during this time

# NTP Server Rotation Use Case

## Ansible

```
cd ansible_playbooks
ansible-playbook -i <your inventory file> change_ntp_servers.yaml
```

## NSO

Sample workflow
```
(venv) ➜  nso-with-ansible git:(nso-with-ansible) ✗ ncs_cli -u admin -C

admin connected from 127.0.0.1 using console on KECORBIN-M-342J
admin@ncs# config t
Entering configuration mode terminal
admin@ncs(config)# load merge nso_cli_scripts/create_device_group.cli
Loading.
53 bytes parsed in 0.01 sec (4.27 KiB/sec)
admin@ncs(config)# load merge nso_templates/ntp_standard.xml
Loading.
920 bytes parsed in 0.02 sec (38.92 KiB/sec)
admin@ncs(config)# commit dry-run
cli {
    local-node {
        data  devices {
             +    template ntp_standard {
             +        config {
             +            cisco-ios-xr:ntp {
             +                server {
             +                    server-list 132.163.96.5;
             +                    server-list 129.6.15.32;
             +                }
             +            }
             +            ios:ntp {
             +                source {
             +                    Loopback 0;
             +                }
             +                server {
             +                    ip {
             +                        peer-list 129.6.15.32;
             +                        peer-list 132.163.95.5;
             +                    }
             +                }
             +            }
             +        }
             +    }
             +    device-group all {
             +        device-name [ nx xe xr ];
             +    }
              }
    }
}
admin@ncs(config)# load merge nso_cli_scripts/change_ntp_servers.cli
Loading.
apply-template-result {
    device nx
    result no-namespace
    info No matching namespaces found for device: nx.
}
apply-template-result {
    device xe
    result ok
}
apply-template-result {
    device xr
    result ok
}
67 bytes parsed in 0.19 sec (342 bytes/sec)
admin@ncs(config)# commit dry-run
cli {
    local-node {
        data  devices {
             +    template ntp_standard {
             +        config {
             +            cisco-ios-xr:ntp {
             +                server {
             +                    server-list 132.163.96.5;
             +                    server-list 129.6.15.32;
             +                }
             +            }
             +            ios:ntp {
             +                source {
             +                    Loopback 0;
             +                }
             +                server {
             +                    ip {
             +                        peer-list 129.6.15.32;
             +                        peer-list 132.163.95.5;
             +                    }
             +                }
             +            }
             +        }
             +    }
             +    device-group all {
             +        device-name [ nx xe xr ];
             +    }
                  device xe {
                      config {
                          ios:ntp {
                              source {
             +                    Loopback 0;
                              }
                              server {
                                  ip {
             +                        peer-list 129.6.15.32 {
             +                        }
             +                        peer-list 132.163.95.5 {
             +                        }
                                  }
                              }
                          }
                      }
                  }
                  device xr {
                      config {
                          cisco-ios-xr:ntp {
                              server {
             +                    server-list 129.6.15.32 {
             +                    }
             +                    server-list 132.163.96.5 {
             +                    }
                              }
                          }
                      }
                  }
              }
    }
}
admin@ncs(config)# commit
```

# TODO

- [x] Topology
- [ ] setup docs/scripts
- [ ] Ansible Playbook
- [ ] "bonus material"
- [ ] Lab Guide
- [ ] Slides
