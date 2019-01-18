# webex-teams notifications

# Installation

1. Install dependencies from `requirements.txt` into your python environment

  ```
  pip install -r requirements.txt
  ```


2. Clone this repository into your NSO's packages directory

3. Compile

  ```
  cd packages/webex-teams/src/
  make clean all
  ```

4. Reload packages from NSO cli

  ```
  packages reload
  ```


# Configuration

The package is configured from inside NSO. Complete the following settings.

```
webex-teams room-id <your room id>
webex-teams api-token <your token>
webex-teams keypath /devices
```

# Credits

This is a generated Python package, made by:

  ncs-make-package --service-skeleton python \
                   --component-class main.Main webex-teams

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
