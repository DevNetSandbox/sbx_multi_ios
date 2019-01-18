# pyats-integration

An example of integrating [Cisco pyATS](https://developer.cisco.com/site/pyats/) with NSO

pyATS makes verifying operational data for devices or services easy.


# Installation

### 1. Clone

clone this repo into your NSO's packages directory

### 2. Install Dependencies

For local installs the NSO python VM runs in whatatver shell `ncs` (venv or otherwise)
was launched from. Make sure and install any necessary python packages
for that interpreter.

For system installations, the global `python` interpreter is used.

`pip install -r requirements.txt`

For more information on this refer to the documentation located at:

`/doc/html/nso_development/ncs.development.pythonvm.nonstdpython.html` on your NSO
instance

### 3. Copy pyATS jobfiles / test cases / testbeds

In this example, the python files are stored in and referenced relative to the NSO's
runtime directory. A sample is available at [./network_tests](./network_tests)


### 4. Compile

Compile your packages

From the package root

```
cd src
make clean all

```

### 5. Reload packages

From NCS CLI (cli-c)

```
packages reload
```

# Usage

The CLI structure is defined via a YANG model located [./src/yang/pyats-integration.yang](./src/yang/pyats-integration.yang)

From the NSO cli, you can run these commands.

Run triggers (code stub, modify to your liking)

```
admin@ncs# pyats triggers trigger name foo
trigger_result

        Triggers brought to you by pyATS/Genie

        Executing trigger foo

```

Run Validations

```
admin@ncs# pyats verifications ?
Possible completions:
  bgp   checks that all bgp neighbors are established
  crc   checks no interfaces have CRC errors
```


## Credits

This is a generated Python package, made by:

  ncs-make-package --service-skeleton python \
                   --component-class main.Main pyats-integration

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
