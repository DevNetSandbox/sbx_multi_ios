#!/bin/bash

# Script used for launching nso in docker container

# see https://medium.com/@gchudnov/trapping-signals-in-docker-containers-7a57fdda7d86

# Enable bash to ping debug messages
set -x

NCS_DIR=/root/nso
NCS_RUN=/root/nso-project

# SIGTERM-handler
term_handler() {
    ncs --stop
    exit 143; # 128 + 15 -- SIGTERM
}

source /root/nso/ncsrc

if [ "$1" == '' ]; then
    cd $NCS_RUN
    # This will kill then tail -f below, and then invoke ncs --stop
    trap 'kill ${!}; term_handler' SIGTERM
    make dev

    #ncs --foreground -v &

    # wait forever
    while true
    do
        tail -f /dev/null & wait ${!}
    done
else
    exec "$@"
fi
