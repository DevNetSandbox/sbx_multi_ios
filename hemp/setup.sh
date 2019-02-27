#!/usr/bin/env bash

echo "Installing Dependencies"

# installing telnet if not present
sudo yum install -y telnet
python3.6 -m venv venv
source venv/bin/activate

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

echo "Deploying Sample VPNs"
ansible-playbook -i inventory.yaml site.yaml
