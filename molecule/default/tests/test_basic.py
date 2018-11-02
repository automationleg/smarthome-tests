import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')
ansible_hosts_file = os.environ['ANSIBLE_ROLES_PATH']+"/basic/files/hosts"


def test_unzip_is_installed(host):
    package = host.package("unzip")
    assert package.is_installed


def test_hosts_file_is_updated(host):
    f = host.file('/etc/hosts')
    content = host.file(ansible_hosts_file).content_string
    assert content in f.content_string
