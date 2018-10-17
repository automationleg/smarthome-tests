import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


def test_apt_transport_https_installed(host):
    package = host.package("apt-transport-https")
    assert package.is_installed


def test_openhab_2_2_0_is_installed(host):
    assert host.package('openhab2').is_installed
    assert host.package('openhab2-addons').is_installed


def test_java8_is_installed(host):
    assert host.package('openjdk-8-jre-headless').is_installed
