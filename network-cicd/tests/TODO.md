# TODO

* the .robot files can be consolidated by passing a variable (testbed) in at runtime
-v --variable name:value *  Set variables in the test data. Only scalar
                         variables with string value are supported and name is
                         given without `${}`. See --escape for how to use
                         special characters and --variablefile for a more
                         powerful variable setting mechanism.
                         Examples:
                         --variable str:Hello       =>  ${str} = `Hello`
                         -v hi:Hi_World -E space:_  =>  ${hi} = `Hi World`
                         -v x: -v y:42              =>  ${x} = ``, ${y} = `42`
