import os
import testinfra
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nameserver_ips(host):
    resolv = host.file("/etc/resolv.conf")
    assert resolv.contains("nameserver 192.168.1.1")
    assert resolv.contains("nameserver 8.8.8.8")


def test_internet_access(host):
    pingres = host.command('ping -c 1 www.google.pl')
    assert pingres.rc == 0, 'No internet access from host!'
