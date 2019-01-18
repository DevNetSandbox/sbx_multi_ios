import ansible_runner

r = ansible_runner.run(private_data_dir='.',
                       inventory='inventory/test.yaml',
                       playbook='site.yaml')
