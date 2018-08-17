# sbx_multiios

Sample code, examples, and resources for use with the [DevNet Multi-IOS Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology)

# setup

Clone this repository

```
git clone --recurse-submodules https://github.com/DevNetSandbox/sbx_multi_ios.git
```


# whats here

A number of different demo environments that can be quickly stood up.

* [GitLab Community Edition](./gitlab/) - Add version control and CI/CD to your sandbox.

* [Network CI/CD Pipeline](./cicd-3tier/) - A core-distribution-access network with a CICD pipeline including GitLab, VIRL, pyATS, and NSO

* [Streaming Telemetry](./metrics-pig/) - Get insights by analyzing large amounts of data through visualizations using streaming telemetry using Pipeline, InfluxDB, and Grafana

* [Log Analytics with ELK](./metrics-elk/) - Use Elasticsearch, Logstash, and Kibana (ELK) for analyzing syslog message from network devices.

# whats not

These are designed to be starting points for future tutorials, and not tutorials themselves.
