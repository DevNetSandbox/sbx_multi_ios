if [ "$HOSTNAME" = devbox ]; then
  echo "Doing some quick reconfiguration of the devbox"
  # update symlink to desired nso version
  sudo rm /opt/nso
  sudo ln -s /opt/nso47 /opt/nso
  source /opt/nso/ncsrc

  # workarounds - sbx needs updating?
  cur_dir=$(pwd)
  sudo mv /opt/nso/packages/services/ncs-4.6-resource-manager-project-3.3.0/packages/*.tar.gz \
          /opt/nso/packages/services/
  cd /opt/nso/packages/services/
  sudo tar zxvf ncs-4.6-resource-manager-3.3.0.tar.gz
  sudo rm *.tar.gz
  sudo rm -rf /opt/nso/packages/services/ncs-4.6-resource-manager-project-3.3.0/
  cd $cur_dir
  sudo mv /opt/nso/etc/ncs/ncs.conf /opt/nso/etc/ncs/ncs.conf.bak
  sudo sh -c 'grep -v "<dir>/opt/nso/packages/neds/</dir>" /opt/nso/etc/ncs/ncs.conf.bak > /opt/nso/etc/ncs/ncs.conf'

  # if we are going to maintain ansible in the python system install we need to make sure
  # it's keeping up to date
  sudo pip uninstall -y ansible


fi

# make sure dependencies are installed and virtualenv is activated
source env_activate.sh

echo "Launching VIRL Simulation"
echo "=========================="
cd virl/sandbox
virl up -e nso --provision --wait-time 15
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
cd ../..

echo ""
echo "Generating pyATS testbed"
echo "==========================="
cd virl/sandbox
virl generate pyats nso -o ../../tests/sandbox_nso_testbed.yaml
cd ../..


echo ""
echo "Execute pyATS tests"
echo "==========================="
cd tests/
easypy eigrp_neighbor_check.py -html_logs . -testbed_file sandbox_nso_testbed.yaml --device headend1 --nbr-count 2
easypy eigrp_neighbor_check.py -html_logs . -testbed_file sandbox_nso_testbed.yaml --device headend2 --nbr-count 2
