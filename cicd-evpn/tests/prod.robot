# Demo Script to verify sanity of network

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        ats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot
Library        unicon.robot.UniconRobot

# we can also import variables from yaml
# Variables      prod_vars.yaml

*** Variables ***
# Defining variables that can be used elsewhere in the test data.
# Can also be driven as dash argument at runtime

# Define the pyATS testbed file to use for this run
${testbed}      ./prod_network.yaml


*** Test Cases ***
# Creating test cases from available keywords.

Initialize
    # Initializes the pyATS/Genie Testbed
    # pyATS Testbed can be used within pyATS/Genie
    use genie testbed "${testbed}"
    connect to device "spine1"
    connect to device "spine2"
    connect to device "leaf1"
    connect to device "leaf2"
    connect to device "leaf3"
    connect to device "leaf4"

# Verify Bgp Neighbors

Verify Bgp neighbors spine1
    verify count "4" "bgp neighbors" on device "spine1"
Verify Bgp neighbors spine2
    verify count "4" "bgp neighbors" on device "spine2"
Verify Bgp neighbors leaf1
    verify count "2" "bgp neighbors" on device "leaf1"
Verify Bgp neighbors leaf2
    verify count "2" "bgp neighbors" on device "leaf2"
Verify Bgp neighbors leaf3
    verify count "2" "bgp neighbors" on device "leaf3"
Verify Bgp neighbors leaf4
    verify count "2" "bgp neighbors" on device "leaf4"


# Verify OSPF neighbor counts
Verify Ospf neighbors spine1
    verify count "4" "ospf neighbors" on device "spine1"
Verify Ospf neighbors spine2
    verify count "4" "ospf neighbors" on device "spine2"
Verify Ospf neighbors leaf1
    verify count "2" "ospf neighbors" on device "leaf1"
Verify Ospf neighbors leaf2
    verify count "2" "ospf neighbors" on device "leaf2"
Verify Ospf neighbors leaf3
    verify count "2" "ospf neighbors" on device "leaf3"
Verify Ospf neighbors leaf4
    verify count "2" "ospf neighbors" on device "leaf4"
