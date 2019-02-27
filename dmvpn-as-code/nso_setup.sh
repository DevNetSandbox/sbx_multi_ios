if [ "$HOSTNAME" = devbox ]; then
  echo "Doing some quick cleanup for sandbox environment"
  # update symlink to desired nso version
  sudo rm /opt/nso
  sudo ln -s /opt/nso47 /opt/nso
  source /opt/nso/ncsrc

  # workaround - sbx needs updating
  cur_dir=$(pwd)
  sudo mv /opt/nso/packages/services/ncs-4.6-resource-manager-project-3.3.0/packages/*.tar.gz \
          /opt/nso/packages/services/
  cd /opt/nso/packages/services/
  sudo tar zxvf ncs-4.6-resource-manager-3.3.0.tar.gz
  sudo rm *.tar.gz
  sudo rm -rf /opt/nso/packages/services/ncs-4.6-resource-manager-project-3.3.0/
  cd $cur_dir
fi

# make sure dependencies are installed and virtualenv is activated
./env_activate.sh

echo "Launching VIRL Simulation"
echo "=========================="
cd virl/sandbox
virl up -e nso --provision
virl nodes nso
cd ../..

# launch NSO
echo "Launching NSO Instance"
echo "=========================="

make nso

# import virl sim devices into NSO
echo "Importing VIRL Simulation into NSO"
echo "=========================="
cd virl/sandbox
virl generate nso nso --syncfrom
cd ../..
cd samples/nso
echo "Deploying DMVPN dmvpn30 via NSO + Ansible"
echo "=========================="
ansible-playbook dmvpn30-playbook.yaml

echo "Deploying DMVPN dmvpn40 via Python + Ansible"
echo "=========================="
python dmvpn40-deploy.py
