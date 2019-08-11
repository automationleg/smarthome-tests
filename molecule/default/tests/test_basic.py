import os
import testinfra
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('vagrant')
ansible_hosts_file = os.environ['HOME']+"/smarthome-devops/oh-data/basic/hosts"

@pytest.mark.parametrize('package',[
    'unzip',
    'htop',
    'python-minimal'
])
def test_unzip_is_installed(host, package):
    package = host.package(package)
    assert package.is_installed


def test_hosts_file_is_updated(host):
    local = testinfra.get_host("ssh://localhost")
    f = host.file('/etc/hosts')
    content = local.file(ansible_hosts_file).content_string
    assert content in f.content_string


def test_timezone_is_set(host):
    f = host.file('/etc/timezone').content_string
    assert 'Europe/Warsaw' in f
