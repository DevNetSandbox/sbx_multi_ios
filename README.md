# sbx_multiios

Sample code, examples, and resources for use with the [DevNet Multi-IOS Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology)

![tile](./static/tile.png "Sandbox Tile")

# setup

### Reserve a sandbox lab.

You can reserve a sandbox lab [here.](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology) During the reservation, you can select "None" for
simulation, as we will be launching the required toplogies as part of the setup.

![reservation](./static/reservation-dialog.png "No topology required")

### Connect to devbox

After your reservation is complete you will receive and email with credential to
connect to the sandbox via VPN.  Once connected.  you can ssh to the devbox using the following credentials. `developer/C1sco12345`

    ssh developer@10.10.20.20

### Clone this repository

```
git clone --recurse-submodules https://github.com/DevNetSandbox/sbx_multi_ios.git
```

### Have fun!

You can now begin working on any of the labs below

# whats here

A number of different lab environments that can be quickly stood up.

* [GitLab Community Edition](./gitlab/) - Add version control and CI/CD to your sandbox.

* [Network CI/CD Pipeline](./network-cicd/) - A complete infrastructure as code pipeline including GitLab, VIRL, pyATS, and NSO

* [Metrics](./netdevops-metrics/) - Get insights by analyzing large amounts of data through visualizations using streaming telemetry

* [Log Analytics](./log-analytics/) - Use ELK stack for analyzing syslog message from network devices.

# whats not

These are designed to be starting points for future tutorials, and not tutorials themselves.
