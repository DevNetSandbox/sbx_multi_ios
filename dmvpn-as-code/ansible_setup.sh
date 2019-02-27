# make sure dependencies are installed and virtualenv is activated
source env_activate.sh

# simulate our target environment in VIRL
echo ""
echo "Launching VIRL Simulation"
echo "=========================="
cd virl/sandbox
virl up -e ansible --provision
virl nodes ansible

# generate ansible inventory for the VIRL sim
virl generate ansible ansible -o ../../inventories/sandbox/main.yaml
cd ../..
echo ""
echo "Generate Ansible Inventory"
echo "==========================="
cat inventories/sandbox/main.yaml

# run the initial ansible deployment (full deployment)
echo ""
echo "Running Ansible Playbook"
echo "==========================="
ansible-playbook -i inventories/sandbox site.yaml
