# log-analytics

Demonstrates how to use ELK Stack to monitor logs from network devices.

## Running / Usage

The entire demo is provided as  a [topology.virl](./topology.virl) you can launch it
by simply typing `virl up` in this directory.

## Network topology

The network topology is provided by virl as defined in [topology.virl](./topology.virl)

![network](./static/network.png)

## Log Analytics - Technology Stack

For log analytics we are using the ELK stack

![elk](./static/stack.png "ELK Stack")

The kibana ui can be found at http://mgmt-ip-of-elk-server:5601
You can find the management IP of the elk server node in your simulation using `virl nodes`

You'll need to add an index pattern of syslog* in the initial Kibana setup, you can also import
the [kibana-dashboard.json](./kibana-dashboard.json) file for some initial visualizations

## Device Configuration

The logging configuration is placed on all the  nodes
via the [topology.virl](./topology.virl) file


### xr1 configuration

```
logging 10.0.0.5 vrf default port 5140
logging source-interface Loopback0

```

### nxos1 configuration

```
logging server 10.0.0.5 port 5140
logging source-interface loopback0
```

### ios1 configuration

```
logging host 10.0.0.5 transport udp port 5140
logging source-interface Loopback0
```
