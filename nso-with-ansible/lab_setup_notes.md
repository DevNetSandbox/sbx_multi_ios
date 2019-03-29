# Introduction to Network Services Orchestrated (NSO) with Ansible

# Topology

we will be using the [virlfiles/xe-xr-nx](https://github.com/virlfiles/xe-xr-nx) topologys

# Pre-reqs

* devnet sbx_multi_ios reservation


# Notes



# Overall Lab Flow (~90 minutes)

1. Lab Logistics / Setup Review (~10min)
2. Lab Setup (~10 min)
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
    5. install ansible
      ```
      python3.6 -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      ```

4. Import devices
    * modify ansible playbook
5. Create device group for all devices
6. create configuration template
7. create compliance report

It should take about 6-7 minutes to boot up these nodes, we can review slides during this time


# TODO

- [x] Topology
- [ ] setup docs/scripts
- [ ] Ansible Playbook
- [ ] "bonus material"
- [ ] Lab Guide
- [ ] Slides
