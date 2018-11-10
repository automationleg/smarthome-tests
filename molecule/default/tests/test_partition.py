import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('krzysr')


def test_root_fs_was_resized(host):
    with host.sudo():
        res = host.command('sudo lvs -o LV_SIZE|grep -v LS').stdout
        assert '25' in res, 'logical volume was not resized'
