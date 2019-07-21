import testinfra
import os

def test_host_is_reachable(host):
    result_code = host.command('hostname').rc
    assert result_code == 0 


def test_openhab_vm_is_reachable_from_main_host(host):
    result_code = host.command('hostname').rc
    assert result_code == 0 

    results = host.command('ssh openhab  service openhab2 status|grep status').stdout
    print(results)
    assert 'SUCCESS' in results


def test_all_openhab_bindings_are_started(host):
    path = os.getcwd()
    # print(path)
    with open(path+'/openhab_features.list') as f:
        features = f.read()
   
    started_features = []
    for line in features.splitlines():
        started_features.append(line.split()[0])

    cmd = 'ssh openhab ssh -p 8101 openhab@localhost "feature:list|grep -v Uninstalled |grep ^openhab"'
    active_features = host.command(cmd).stdout
    # not_started_features = [
    #     feature
    #     for feature in features
    #     if feature not in active_features
    # ]
    not_started_features = []
    for feature in started_features:
       if feature not in active_features:
           not_started_features.append(feature)
    
    assert not_started_features == [], f'Not all openhab features started. features not started: {not_started_features}'