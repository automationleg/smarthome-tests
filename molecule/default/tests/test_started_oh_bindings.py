import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


def test_all_openhab_bindings_are_started(host):
    path = os.fspath.join('..')
    with open(path+'/openhab_features.list') as f:
        features = f.read()
   
    started_features = []
    for line in features.splitlines():
        started_features.append(line.split()[0])

    cmd = 'ssh -p 8101 openhab@localhost "feature:list|grep -v Uninstalled |grep ^openhab"'
    active_features = host.command(cmd).stdout
    # not_started_features = [
    #     feature
    #     for feature in features
    #     if feature not in active_features
    # ]
    
    for feature in started_features:
       if feature not in active_features:
           not_started_features.append(feature)
    
    assert not_started_features, 'Not all openhab features started. features not started: '+not_started_features

    

