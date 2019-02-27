# simulate our target environment in VIRL
echo "Launching VIRL Simulation"
echo "=========================="
cd virl/sandbox
virl up -e ansible --provision
virl nodes

# generate ansible inventory for the VIRL sim
virl generate ansible ansible -o ../../inventories/sandbox/main.yaml
cd ../..
echo "Ansible Generated Inventory"
echo "==========================="
cat inventories/sandbox/main.yaml

# run the initial ansible deployment (full deployment)
echo "Running Ansible Playbook"
echo "==========================="
ansible-playbook -i inventories/sandbox site.yaml
