#!/usr/bin/env bash

# installing telnet if not present
sudo yum install -y telnet

echo "Launching VIRL simulation ... "
root_dir=$(pwd)
virl up --provision


echo "Launching NSO ... "
cd nso
ncs-setup --dest . --package cisco-ios
cd packages/vpn/src
make clean all
cd $root_dir/nso
ncs
cd $root_dir

echo "Importing network to NSO .. "
virl generate nso 2>&1

echo "Performing initial sync of devices..."
echo "devices sync-from" | ncs_cli -u admin -C

echo "Network Summary"
cd $root_dir
virl ls
virl nodes


docker-compose up -d

echo "Services Summary"
docker-compose ps
