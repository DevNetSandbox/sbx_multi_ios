cd nso
ncs --stop
rm -rf ncs-cdb/ state target storedstate ncs.conf logs
cd ..
virl down
