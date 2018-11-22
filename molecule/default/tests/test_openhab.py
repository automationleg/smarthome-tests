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


def test_openhab_is_listening_on_http_port_8080(host):
    assert host.socket("tcp://:::8080").is_listening


def test_openhab_is_listening_on_ssl_port_8443(host):
    assert host.socket("tcp://:::8443").is_listening


def test_openhab_web_is_accessible(host):
    cmd = 'curl -L 192.168.1.23:8080'
    result = host.command(cmd).stdout
    assert '<title>openHAB</title>' in result
