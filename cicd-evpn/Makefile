export PYTHONPATH=$(shell pwd)
# this loosely resembles magic
# https://stackoverflow.com/questions/17834582/run-make-in-each-subdirectory
TOPTARGETS := test

SUBDIRS := $(wildcard tests/*/.)

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
		$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS) setup.mk

harness-test:
	echo  ########### ####### ${PYTHONPATH}
	-easypy deployment_harness.py \
		-testbed_file tests/test_network.yaml \
		-html_logs . \
		-playbook site.yaml \
		-inventory inventory/test.yaml

harness-prod:
	echo  ########### ####### ${PYTHONPATH}
	-easypy deployment_harness.py \
		-testbed_file tests/prod_network.yaml \
		-html_logs . \
		-playbook site.yaml \
		-inventory inventory/prod.yaml


prep:
	-osascript window_layout.scpt

clean:  netsim-clean nso-clean ansible-clean

dev: netsim nso sync-from deploy-dev

netsim:

	-@ncs-netsim --dir netsim create-device cisco-nx spine1
	-@ncs-netsim --dir netsim add-device cisco-nx spine2
	-@ncs-netsim --dir netsim add-device cisco-nx leaf1
	-@ncs-netsim --dir netsim add-device cisco-nx leaf2
	-@ncs-netsim --dir netsim add-device cisco-nx leaf3
	-@ncs-netsim --dir netsim add-device cisco-nx leaf4
	-@ncs-netsim start


nso:
	-@rm -rf packages/*.tar.gz
	-make packages
	-@ncs-setup --dest . --package cisco-nx --package resource-manager
	-@echo "Starting local NSO instance..."
	-@ncs

ansible-clean:
	-@rm *.retry > /dev/null

netsim-clean:
	-@echo "Stopping All Netsim Instances..."
	-@killall confd
	-@rm -Rf netsim/
	-@rm README.netsim

nso-clean:
	-@echo "Stopping NSO..."
	-@ncs --stop
	-@rm -Rf README.ncs agentStore state.yml logs/ ncs-cdb/ ncs-java-vm.log ncs-python-vm.log ncs.conf state/ storedstate target/

verify-prod:
		-cd tests
		PYTHONPATH=$PYTHONPATH:$PWD
		-robot tests/prod.robot
    # important: need to add our current directory to PYTHONPATH
    # -robot prod.robot

verify-test:
		-cd tests
		PYTHONPATH=$PYTHONPATH:$PWD
		-robot tests/test.robot
    # important: need to add our current directory to PYTHONPATH
    #-robot test.robot

ssh:
	ssh admin@prod-nso -p 2024

deploy-dev:
	-@ansible-playbook -i inventory/dev.yaml site.yaml

deploy-prod:
	-@ansible-playbook -i inventory/prod.yaml site.yaml

deploy-test:
	-@ansible-playbook -i inventory/test.yaml site.yaml

sync-from:
	-@echo "Performing devices sync-from..."
	-@curl -X POST -u admin:admin http://localhost:8080/api/running/devices/_operations/sync-from

# EXPERIMENTAL: Docker support
docker:
	-docker stop cicd-evpn
	-docker rm cicd-evpn
	-docker build -t cicd-evpn .
	-docker run -ti cicd-evpn /bin/bash

docker-image:
	-docker build -f Dockerfile.nso --build-arg NSOVER=4.7 -t nso-base .

docker-run:
	-docker run -ti -p 8080:8080 -p 2022:2022 -p 2023:2023 nso-base /bin/bash
