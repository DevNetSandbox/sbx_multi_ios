#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
cd tests/crc_errors
make test
