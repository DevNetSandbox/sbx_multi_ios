# some handy make targets is always nice...

# always a good idea with genie+robot
PYTHONPATH = $PYTHONPATH:$(pwd)

test:
	-easypy CRC_check_job.py -html_logs . -testbed_file ../default_testbed.yaml
	-open TaskLog.html

robot:
	robot --variable testbed:../default_testbed.yaml interface.robot

clean:
	-rm -Rf archive/ runinfo/ __pycache__ log.html output.xml report.html
