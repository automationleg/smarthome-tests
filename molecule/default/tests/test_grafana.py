import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('vagrant')


def test_grafana_docker_is_running(host):
    cmd = "sudo docker ps| grep grafana"
    result = host.command(cmd).stdout
    assert 'Up' in result, 'Grafana container is not running!'


def test_if_grafana_is_listening_on_port_3000(host):
    assert host.socket("tcp://:::3000").is_listening


def test_grafana_web_is_accessible(host):
    cmd = 'curl -L openhab:3000'
    result = host.command(cmd).stdout
    assert '<title>Grafana</title>' in result
