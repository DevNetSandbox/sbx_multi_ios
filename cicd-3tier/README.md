# cicd-3tier

Use Gitlab to create a full CI-CD pipeline for a standard 3 Tier, Core > Distribution > Access, topology.  The Core is composed of 2 IOS XE routers, Distribution and Access are Open NX-OS switches.  

## Prerequisites

This lab requires you to have the [gitlab stack](../gitlab) running on your devbox


## Network topology

The network topology for both test and prod is provided by virl as defined in [./virl/test/topology.virl](./virl/test/topology.virl) and [./virl/prod/topology.virl](./virl/prod/topology.virl)

![network](./static/topology.png)

## Pipeline Technology Stack

![pipeline](./static/pipeline.png "CICD Pipeline")

## Setup

This following script should cover all the initial installation:

```
./setup.sh
```


## Getting started

You should be able to see your infrastructure as code repository at http://10.10.20.50/developer/cicd-3tier


## Known issues

### VIRL node boot error

Occasionally, a node may not boot up correctly and you will see an error similar to
this:

```
sync-result {
    device test-dist2
    result false
    info Failed to connect to device test-dist2: connection refused: No route to host (Host unreachable)
}
```

To fix this you can use virlutils to stop/start the node e.g

```
cd virl/test
virl stop test-dist2
virl start test-dist2
```

### Initial Configuration Pushes from GitLab may fail

Occasionally the initial configuration pushes from GitLab to the networks may start before the nodes are fully ready, and one or more may timeout.  This can result in the initial configuration and connectivity in the topology from not coming up automatically after running `setup`.  

The most common operational issue is the VPC domain not coming up correctly between the dist nodes.  Troubleshoot using CLI, but these steps tend to work.  (Maybe needed on test, prod, or both)

1. SSH to both `dist1` and `dist2` and shutdown the VPC peerlink and VPC to `access1`

    ```
    conf t
    int po1
    shut
    int po11
    shut
    ```

1. Wait about a minute for everything to settle, and then reenable the peer-link on both switches.  

    ```
    int po1
    no shut
    ```

1. Once `show vpc` shows adjacency healthy on both dist switches, bring up the link to access1

    ```
    int po11
    no shut
    ```

1. If VPC is not healthy on the distribution layer, the pyATS test will fail many of the tests as they are written to expect a healthy network.  


## Verification / Troubleshooting

If all goes well, you should see output similar to this

```
[developer@devbox cicd-3tier]$./setup.sh
Launching VIRL simulations (prod+test) ...
Creating default environment from topology.virl
Waiting 10 minutes for nodes to come online....
  [####################################]  100%             
Launching NSO ...
Importing Test network to NSO ..
Updating NSO....
Successfully added VIRL devices to NSO
Importing Prod network to NSO
Updating NSO....
Successfully added VIRL devices to NSO
Performing initial sync of devices...
sync-result {
    device access1
    result true
}
sync-result {
    device core1
    result true
}
sync-result {
    device core2
    result true
}
sync-result {
    device dist1
    result true
}
sync-result {
    device dist2
    result true
}
sync-result {
    device test-access1
    result true
}
sync-result {
    device test-core1
    result true
}
sync-result {
    device test-core2
    result true
}
sync-result {
    device test-dist1
    result true
}
sync-result {
    device test-dist2
    result true
}
Creating Repo on Gitlab
Configure Git
Initalizing Local Repository
Initialized empty Git repository in /home/developer/sbx_multi_ios/cicd-3tier/.git/
Switched to a new branch 'test'
[test (root-commit) ba69843] Initial commit
 24 files changed, 3540 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 .gitlab-ci.yml
 create mode 100644 README.md
 create mode 100755 cleanup.sh
 create mode 100644 group_vars/all.yaml
 create mode 100644 host_vars/access1.yaml
 create mode 100644 host_vars/core1.yaml
 create mode 100644 host_vars/core2.yaml
 create mode 100644 host_vars/dist1.yaml
 create mode 100644 host_vars/dist2.yaml
 create mode 100644 inventory/prod.yaml
 create mode 100644 inventory/test.yaml
 create mode 100755 setup.sh
 create mode 100644 site.yaml
 create mode 100644 static/pipeline.png
 create mode 100644 tests/prod.robot
 create mode 100644 tests/prod_testbed.yml
 create mode 100644 tests/reachability/__init__.py
 create mode 100644 tests/reachability/pyats_job.py
 create mode 100644 tests/reachability/pyats_loopback_reachability.py
 create mode 100644 tests/test.robot
 create mode 100644 tests/test_testbed.yml
 create mode 100644 virl/prod/topology.virl
 create mode 100644 virl/test/topology.virl
Pushing Branches
Counting objects: 35, done.
Delta compression using up to 5 threads.
Compressing objects: 100% (30/30), done.
Writing objects: 100% (35/35), 356.63 KiB | 0 bytes/s, done.
Total 35 (delta 7), reused 0 (delta 0)
To http://developer:C1sco12345@10.10.20.50/developer/cicd-3tier.git
 * [new branch]      test -> test
Branch test set up to track remote branch test from origin.
Switched to a new branch 'production'
Total 0 (delta 0), reused 0 (delta 0)
remote:
remote: To create a merge request for production, visit:
remote:   http://gitlab/developer/cicd-3tier/merge_requests/new?merge_request%5Bsource_branch%5D=production
remote:
To http://developer:C1sco12345@10.10.20.50/developer/cicd-3tier.git
 * [new branch]      production -> production
Branch production set up to track remote branch production from origin.
Switched to branch 'test'
Test Network Summary
Running Simulations
╒═════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation          │ Status   │ Launched                   │ Expires   │
╞═════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ test_default_ldTwiU │ ACTIVE   │ 2018-08-15T04:18:26.886231 │           │
╘═════════════════════╧══════════╧════════════════════════════╧═══════════╛
Here is a list of all the running nodes
╒══════════════╤═════════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node         │ Type        │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞══════════════╪═════════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ test-dist1   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.213        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-access1 │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.215        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-dist2   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.214        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-core2   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.212        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-core1   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.211        │ N/A                │
╘══════════════╧═════════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛
Production Network Summary
Running Simulations
╒═════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation          │ Status   │ Launched                   │ Expires   │
╞═════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ prod_default_ZufsKU │ ACTIVE   │ 2018-08-15T04:18:27.136267 │           │
╘═════════════════════╧══════════╧════════════════════════════╧═══════════╛
Here is a list of all the running nodes
╒═════════╤═════════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node    │ Type        │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞═════════╪═════════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ core1   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.221        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ access1 │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.225        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ dist1   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.223        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ core2   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.222        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ dist2   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.224        │ N/A                │
╘═════════╧═════════════╧═════════╧═════════════╧════════════╧══════════════════════╧═══════════════════╛
```

# Setting up a Local Development Environment
To experience and demonstrate the full NetDevOps configuration pipeline, you may want to setup a local development environment where you can test proposed configuration changes before committing and pushing them to GitLab for the full test builds to occur.  To complete this step you will need to have a few local pre-requisites setup on your local workstation.  

## Local Development Environment Prerequisites
### Network Service Orchestrator
In order to test the configuration pipeline locally, you'll need to have a local install of NSO on your workstation.  Furthermore, you'll need to have the same versions of NSO and NEDs installed as the DevBox within the Sandbox.  Using different versions **may** work, but for best experience matching the versions exactly is recommended.  

* Network Service Orchestrator 4.5.3
* Cisco IOS NED 5.8
* Cisco IOS XE NED 6.2.10
* Cisco NX-OS NED 4.5.10

Once you have installed these versions, you'll need to `source` the `ncsrc` file for this version before beginning the local dev process.  

> Note: Details on how to install NSO locally are beyond the scope of this README.

### Python + Ansible
The Network as Code mechanism in this demonstration leverages both Ansible and NSO, with Ansible orchestrating the execution and configuration used by NSO to deploy to the network.  In order to test locally, you'll need to have a Python environment (virtual environment recommended) that meets these requirements.  

* Python 3.6.x (3.6.5 or higher recommended)
    * *Python 2.7 would likely work, but the time to move to Python 3 has arrived.*
* Ansible 2.6.3 or higher

A `requirements.txt` file is included in the repository.  Simply `pip install -r requirements.txt` to get started.  

## "Making" the Dev Environment
With the pre-requisites under control, follow these steps to setup your local dev environment.  

1. Clone a copy of the repository from GitLab to your local workstation.  Use this command to ensure the demo credentials are embedded in the git configuration.  

    ```bash
    git clone http://developer:C1sco12345@10.10.20.50/developer/cicd-3tier
    cd cicd-3tier
    ```

2. To simplify the setup and management of the local environment, a `Makefile` is included in the repository.  Simply `make dev` to do the following. (To see the exact commands being executed for each of these steps, just take a look at the contents of [`Makefile`](Makefile))
    1. Use NCS NetSim to start a local simulation of the network including the core, distribution, and access devices.
    2. Setup a local NCS project directory within the repo.
    3. Start NCS and import in the netsim simulation.
    4. Perform an initial `sync-from`.
    5. Deploy the current "Network as Code" configuration to NCS and the network devices using Ansible.

    ```bash
    # Sample output
    $ make dev

    ncs-netsim --dir netsim create-device cisco-ios core1
    DEVICE core1 CREATED
    ncs-netsim --dir netsim add-device cisco-ios core2
    DEVICE core2 CREATED
    ncs-netsim --dir netsim add-device cisco-nx dist1
    DEVICE dist1 CREATED
    ncs-netsim --dir netsim add-device cisco-nx dist2
    DEVICE dist2 CREATED
    ncs-netsim --dir netsim add-device cisco-nx access1
    DEVICE access1 CREATED
    ncs-netsim start
    DEVICE core1 OK STARTED
    DEVICE core2 OK STARTED
    DEVICE dist1 OK STARTED
    DEVICE dist2 OK STARTED
    DEVICE access1 OK STARTED
    ncs-setup --dest . --package cisco-ios --package cisco-nx
    Using netsim dir /Users/hapresto/coding/temp/cicd-3tier/netsim
    ncs
    curl -X POST -u admin:admin http://localhost:8080/api/running/devices/_operations/sync-from
    <output xmlns='http://tail-f.com/ns/ncs'>
      <sync-result>
        <device>access1</device>
        <result>true</result>
      </sync-result>
      <sync-result>
        <device>core1</device>
        <result>true</result>
      </sync-result>
      <sync-result>
        <device>core2</device>
        <result>true</result>
      </sync-result>
      <sync-result>
        <device>dist1</device>
        <result>true</result>
      </sync-result>
      <sync-result>
        <device>dist2</device>
        <result>true</result>
      </sync-result>
    </output>
    ansible-playbook --syntax-check -i inventory/dev.yaml site.yaml

    playbook: site.yaml
    ansible-playbook -i inventory/dev.yaml site.yaml

    PLAY [Check Synchronization of Devices] ******

    TASK [check-sync] ***********************
    changed: [localhost]

    PLAY [Verify device configuration] ***********************

    TASK [Device configuration] ***************
    changed: [core2]
    changed: [core1]
    changed: [access1]
    changed: [dist1]
    changed: [dist2]

    PLAY [Push Desired Configuration to Devices] ************

    TASK [NSO sync-to action] ***********************
    changed: [localhost]

    PLAY RECAP ***************************
    access1                    : ok=1    changed=1    unreachable=0    failed=0
    core1                      : ok=1    changed=1    unreachable=0    failed=0
    core2                      : ok=1    changed=1    unreachable=0    failed=0
    dist1                      : ok=1    changed=1    unreachable=0    failed=0
    dist2                      : ok=1    changed=1    unreachable=0    failed=0
    localhost                  : ok=2    changed=2    unreachable=0    failed=0
    ```

3. Now go ahead and open issues, create branches, make changes to the config, etc.  Then, before running `git add/commit/push`, you can test locally with `make dev-deploy`.

    ```bash
    $ make dev-deploy
    ansible-playbook --syntax-check -i inventory/dev.yaml site.yaml

    playbook: site.yaml
    ansible-playbook -i inventory/dev.yaml site.yaml

    PLAY [Check Synchronization of Devices] ******

    TASK [check-sync] ***********************
    changed: [localhost]

    PLAY [Verify device configuration] ***********************

    TASK [Device configuration] ***************
    changed: [core2]
    changed: [core1]
    changed: [access1]
    changed: [dist1]
    changed: [dist2]

    PLAY [Push Desired Configuration to Devices] ************

    TASK [NSO sync-to action] ***********************
    changed: [localhost]

    PLAY RECAP ***************************
    access1                    : ok=1    changed=1    unreachable=0    failed=0
    core1                      : ok=1    changed=1    unreachable=0    failed=0
    core2                      : ok=1    changed=1    unreachable=0    failed=0
    dist1                      : ok=1    changed=1    unreachable=0    failed=0
    dist2                      : ok=1    changed=1    unreachable=0    failed=0
    localhost                  : ok=2    changed=2    unreachable=0    failed=0
    ```

    * Alternatively you can manually run the `ansible-playbook` commands to lint and then run the playbook.  

        ```bash
        ansible-playbook --syntax-check -i inventory/dev.yaml site.yaml
        ansible-playbook -i inventory/dev.yaml site.yaml
        ```

## Cleaning Up the Local Dev Environment
When you are ready to shutdown the local dev environment, simply `make clean` to shut down netsim and NSO and erase their remnants.  

```bash
$ make clean

ncs --stop
rm -Rf README.ncs logs/ ncs-cdb/ ncs-java-vm.log ncs-python-vm.log ncs.conf packages/ state/ storedstate target/
ncs-netsim stop
DEVICE core1 STOPPED
DEVICE core2 STOPPED
DEVICE dist1 STOPPED
DEVICE dist2 STOPPED
DEVICE access1 STOPPED
rm -Rf netsim/
rm README.netsim
```
