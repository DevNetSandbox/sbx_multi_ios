# vpc-distribution

This package provides the ability to quickly provision a standard VPC distribution
architecture.


# Sample Instance

```
vpc-distribution BLOCK1
 aggregate-prefix 172.16.0.0/16
 distribution dist1
  connection-to access1
   interface 1/1
  !
 !
 distribution dist2
  connection-to access1
   interface 1/2
  !
 !
 access_pair BLOCK1-ROW1
  switches access1
   connection-to dist1
    interface 1/1
   !
   connection-to dist2
    interface 1/2
   !
  !
 !
!
```


# Credits

This is a generated Python package, made by:

  ncs-make-package --service-skeleton python-and-template \
                   --component-class main.Main vpc-distribution

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
