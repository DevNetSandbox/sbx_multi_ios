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
