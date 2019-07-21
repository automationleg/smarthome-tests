import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


def test_all_openhab_bindings_are_started(host, request):
    path = request.fspath.dirname
    with open(path+'/openhab_features.list') as f:
        features = f.read()
   
    expected_started_features = [
        line.split()[0]
        for line in features.splitlines()
    ]

    cmd = 'ssh -p 8101 openhab@localhost "feature:list|grep -v Uninstalled |grep ^openhab"'
    response = host.command(cmd).stdout

    # remove strange utf8 characters from the ssh response
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    active_features = ansi_escape.sub('', response)

    not_started_features = [
        feature
        for feature in expected_started_features
        if feature not in active_features
    ]
    
    assert len(not_started_features) == 0, 'Not all openhab features started. features not started: {}'.format(not_started_features)
    