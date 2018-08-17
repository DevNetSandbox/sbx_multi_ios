dev: netsim sync-from

sync-from:
	-curl -X POST -u admin:admin http://localhost:8080/api/running/devices/_operations/sync-from

netsim:

	-ncs-netsim --dir netsim create-device cisco-ios core1
	-ncs-netsim --dir netsim add-device cisco-ios core2
	-ncs-netsim --dir netsim add-device cisco-nx dist1
	-ncs-netsim --dir netsim add-device cisco-nx dist2
	-ncs-netsim start
