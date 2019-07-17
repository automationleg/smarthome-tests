import testinfra

def test_host_is_reachable(host):
    result_code = host.command('hostname').rc
    assert result_code == 0 


def test_openhab_vm_is_reachable_from_main_host(host):
    result_code = host.command('hostname').rc
    assert result_code == 0 

    results = host.command('ssh openhab  service openhab2 status|grep status').stdout
    print(results)
    assert 'SUCCESS' in results