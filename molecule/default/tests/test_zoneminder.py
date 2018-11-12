import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


@pytest.mark.parametrize('container', [
    'mysql',
    'zoneminder'
])
def test_mysql_docker_is_running(host, container):
    cmd = "sudo docker ps| grep "+container
    result = host.command(cmd).stdout
    assert 'Up' in result, container+' container is not running!'


@pytest.mark.parametrize('container, socket', [
    ('mysql','tcp://:::8306'),
    ('zoneminder','tcp://:::8099')
])
def test_if_zoneminder_is_listening(host, container, socket):
    assert host.socket(socket).is_listening, container+'\
            is not listening on port '+socket
