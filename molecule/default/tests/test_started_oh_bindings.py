import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


def test_all_openhab_bindings_are_started(host):
    with open('openhab_features.list') as f:
        features = f.read()
   
    started_features = []
    for line in features.splitlines():
        started_features.append(line.split()[0])

    host.command('') 
    

