clean: clean-docker clean-virl

clean-stack:
	-@docker-compose -f telemetry-stack/docker-compose.yaml down

clean-virl:
	-@virl down
	-@rm -Rf .virl/

lab: stack virl stack-status

stack: stack-build stack-up

stack-up:
	docker-compose -f telemetry-stack/docker-compose.yaml up -d

stack-build:
	docker-compose -f telemetry-stack/docker-compose.yaml build

stack-status:
	docker-compose -f telemetry-stack/docker-compose.yaml ps

tap:
	docker-compose -f telemetry-stack/docker-compose.yaml exec unified-pipeline tail -n 1000 telemetry_model_raw.txt

virl:
	@virl up --provision

# clean: clean-netsim clean-nso clean-virl
#
# clean-virl:
# 	-@virl down
# 	-@rm -Rf .virl/
#
# clean-netsim:
# 	-@echo "Stopping All Netsim Instances..."
# 	-@killall confd
# 	-@rm -Rf netsim/
# 	-@rm README.netsim
#
# clean-nso:
# 	-@echo "Stopping NSO..."
# 	-@ncs --stop
# 	-@rm -Rf README.ncs agentStore state.yml logs/ ncs-cdb/ ncs-java-vm.log ncs-python-vm.log ncs.conf state/ storedstate target/
#
# dev: deps netsim nso
#
# deps:
# 	./lab_prep.sh && python3.6 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
#
#
# netsim:
# 	-@ncs-netsim --dir netsim create-device cisco-ios xe
# 	-@ncs-netsim --dir netsim add-device cisco-iosxr xr
# 	-@ncs-netsim --dir netsim add-device cisco-nx nx
# 	-@ncs-netsim start
#
# nso:
# 	ncsc -c packages/pipe-yaml/yaml-c.cli -o packages/yaml-c.ccl
# 	ncs-setup --dest . --package cisco-ios --package cisco-iosxr --package cisco-nx
# 	export PATH=$$PATH:packages/pipe-yaml; echo $$PATH; ncs
#
# test: clean-netsim clean-nso deps virl nso virl
#
# virl: nso
# 	@virl up --provision
# 	virl generate nso --syncfrom
