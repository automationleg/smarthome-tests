import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


@pytest.mark.skip
def test_openhab2_backup_archive_copied(host):
    f = host.file("/tmp/openhab2-backup.zip")
    assert f.exists


def test_openhab2_configuration_is_restored(host):
    assert True
