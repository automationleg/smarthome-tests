import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


def get_grafana_auth_string():
    user = 'admin'
    passw = 'grafana321'


def execute_influx_command(host, command):
    auth = get_influx_auth_string()
    cmd = auth+'-execute \''+command+'\''
    result = host.command(cmd)
    assert result.rc == 0, 'Command execution failed'
    return result.stdout


def test_grafana_docker_is_running(host):
    cmd = "sudo docker ps| grep grafana"
    result = host.command(cmd).stdout
    assert 'Up' in result, 'Grafana container is not running!'


def test_if_grafana_is_listening_on_port_3000(host):
    assert host.socket("tcp://:::3000").is_listening
