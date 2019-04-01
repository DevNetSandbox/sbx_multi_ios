devenv:
	-osascript window_layout.scpt


all: clean netsim nso
clean:  netsim-clean nso-clean

netsim:
	-@ncs-netsim --dir netsim create-device cisco-ios headend1
	-@ncs-netsim --dir netsim add-device cisco-ios headend2
	-@ncs-netsim --dir netsim add-device cisco-ios remote3
	-@ncs-netsim --dir netsim add-device cisco-ios remote4
	-@ncs-netsim start

netsim-clean:
	-@ncs-netsim stop
	-@rm -rf netsim

ansible-clean:
	-rm site.retry
	-rm inventories/sandbox.yaml

nso-clean:
	-@echo "Stopping NSO..."
	-@ncs --stop
	-@rm -Rf README.ncs agentStore state.yml logs/ ncs-cdb/ ncs-java-vm.log ncs-python-vm.log ncs.conf state/ storedstate target/

nso:
	ncs-setup --dest . --package cisco-ios --package ${NCS_DIR}/packages/services/resource-manager
	-@echo "Starting local NSO instance..."
	-@ncs
