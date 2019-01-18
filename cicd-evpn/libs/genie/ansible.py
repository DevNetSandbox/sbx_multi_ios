from ats import aetest
from pyats.log.utils import banner
import logging
from genie.harness.base import Trigger
import ansible_runner

log = logging.getLogger()


class RunAnsiblePlaybook(Trigger):

    @aetest.test
    def run_playbook(self, uut, playbook, inventory):
        """Runs an Ansible playbook"""

        msg = "Running Ansible Playbook {} with {}"
        log.info(banner(msg.format(playbook, inventory)))
        r = ansible_runner.run(private_data_dir='.',
                               inventory=inventory,
                               playbook=playbook)

        log.info("Playbook status: {}".format(r.stats))
