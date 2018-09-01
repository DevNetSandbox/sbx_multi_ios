dev: netsim nso sync-from dev-deploy

clean: nso-clean netsim-clean

netsim:

	-ncs-netsim --dir netsim create-device cisco-ios core1
	-ncs-netsim --dir netsim add-device cisco-ios core2
	-ncs-netsim --dir netsim add-device cisco-nx dist1
	-ncs-netsim --dir netsim add-device cisco-nx dist2
	-ncs-netsim --dir netsim add-device cisco-nx access1
	-ncs-netsim start

netsim-clean:
	-ncs-netsim stop
	-rm -Rf netsim/
	-rm README.netsim

nso:
	-ncs-setup --dest . --package cisco-ios --package cisco-nx
	-ncs

nso-clean:
	-ncs --stop
	-rm -Rf README.ncs logs/ ncs-cdb/ ncs-java-vm.log ncs-python-vm.log ncs.conf packages/ state/ storedstate target/

sync-from:
	-curl -X POST -u admin:admin http://localhost:8080/api/running/devices/_operations/sync-from

dev-deploy:
	-ansible-playbook --syntax-check -i inventory/dev.yaml site.yaml
	-ansible-playbook -i inventory/dev.yaml site.yaml
