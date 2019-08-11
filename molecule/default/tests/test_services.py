import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('vagrant')


@pytest.mark.parametrize('service',[
    'openhab2',
    'influxdb',
    'vcontrold',
    'docker'
])
def test_smarthome_services_are_enabled(host, service):
    assert host.service(service).is_enabled
    assert host.service(service).is_running
