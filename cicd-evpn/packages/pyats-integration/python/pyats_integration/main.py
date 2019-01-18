# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.dp import Action
import subprocess


class CheckBGPNeighbors(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        self.log.info('action name: ', name)
        self.log.info("Directory: {}".format(subprocess.check_output(['pwd'])))
        results = subprocess.check_output(['./tests/run_bgp_tests.sh'])
        output.test_results = results.decode('utf-8')


class CheckCRCErrors(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        self.log.info('action name: ', name)
        self.log.info("Directory: {}".format(subprocess.check_output(['pwd'])))
        results = subprocess.check_output(['./tests/run_crc_tests.sh'])
        output.test_results = results.decode('utf-8')


class RunTrigger(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        self.log.info('Running Genie Trigger: ', input.name)

        output.trigger_result = """

        Triggers brought to you by pyATS/Genie

        Executing trigger {}
        """.format(input.name)


class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')
        self.register_action('check-bgp-action', CheckBGPNeighbors)
        self.register_action('check-crc-action', CheckCRCErrors)
        self.register_action('run-trigger-action', RunTrigger)

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
