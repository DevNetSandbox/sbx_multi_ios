#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
cd tests/bgp_adjacencies
make test
