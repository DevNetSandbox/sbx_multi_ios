# DMVPN

This directory contains an NSO service model for configuring and maintaining
DMVPN clouds.  It currently is only implemented for cisco-ios devices, but can be
extended to support other Cisco, or 3rd party devices easily.

## Model

A service model provides three high level capabilities.


  * A data model which describes the service, and it's associated parameters,
  validations, and constraints. This data model is used to generate the various interfaces
  to the service, these include CLI, UI as well as API's (NetConf, RESTConf, REST, etc)

  The primary data model for our DMVPN service is expressed in YANG and can be found
  [here](./src/yang/dmvpn.yang)

  * Configuration Templates  which can be applied to
  devices during service instantiation, as well as operations.

  The templates used in this POC can be found [here](./templates)

  * Logic - logic that controls which templates need to be applied to which devices.  
  This POC uses python to provide this logic, and the various scripts can be found [here](./python)

  The templates used in this POC can be found [here](./templates)


## Background

The initial skeleton for this code was auto-generated Python package, made by:

  ncs-make-package --service-skeleton python-and-template \
                   --component-class main.Main dmvpn

It contains a dummy YANG model which implements a minimal Service
and an Action that doesn't really do anything useful. They are
there just to get you going.

You will also find two test cases in:

  test/internal/lux/service/
  test/internal/lux/action/

that you can run if you have the 'lux' testing tool.
Your top Makefile also need to implement some Make targets
as described in the Makefiles of the test cases.
You can also just read the corresponding run.lux tests and
do them manually if you wish.

The 'lux' test tool can be obtained from:

  https://github.com/hawk/lux.git
