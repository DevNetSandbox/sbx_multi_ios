base_dir=$(pwd)

ncs --stop
ncs-setup --reset
ncs-netsim stop
ncs-netsim delete-network
rm -rf netsim inventory.yaml packages state target scripts logs ncs-cdb storedstate README.netsim README.ncs ncs.conf


cd $base_dir/virl/test/
virl down
cd $base_dir/virl/prod/
virl down
