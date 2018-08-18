#!/usr/bin/env bash

# a quick script to import all the virl nodes to your local box. useful when
# you want to use your own PC...

cd virl/test
virl use $(virl id)
cd ../prod
virl use $(virl id)


echo "
you can now use virl commands against either test or
prod depending on your directory

e.g

cd virl/test
virl nodes

cd ../prod
virl nodes

"
