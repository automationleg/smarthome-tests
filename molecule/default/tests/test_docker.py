import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


def test_docker_is_installed(host):
    package = host.package("docker-ce")
    assert package.is_installed


def test_docker_service_is_running(host):
    service = host.service('docker')
    assert service.is_running
