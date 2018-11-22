import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('openhab')


def get_influx_auth_string():
    user = 'adminkr'
    passw = 'SuperSecretPassword123'
    db = 'openhab_db'
    auth = 'influx -username '+user+' -password '+passw+' -database '+db+' '
    return auth


def execute_influx_command(host, command):
    auth = get_influx_auth_string()
    cmd = auth+'-execute \''+command+'\''
    result = host.command(cmd)
    assert result.rc == 0, 'Command execution failed'
    return result.stdout


def test_influxdb_is_installed(host):
    package = host.package("influxdb")
    assert package.is_installed


def test_influxdb_service_is_running(host):
    service = host.service('influxdb')
    # assert service.is_enabled
    assert service.is_running


def test_influxdb_is_listening_on_port_8086(host):
    assert host.socket("tcp://:::8086").is_listening


@pytest.mark.skip
def test_influxdb_config_file_updated(host):
    config = host.file('/etc/influxdb/influxdb.conf')
    hostname = host.command('hostname').stdout.replace('\n', '')
    text = 'hostname = \"'+hostname+'\"'
    assert config.contains(text)


def test_influxdb_python_client_is_installed(host):
    pkg = host.pip_package.get_packages(pip_path='/usr/bin/pip3')
    assert 'influxdb' in pkg


def test_openhab_db_is_created(host):
    cmd = 'show databases'
    result = execute_influx_command(host, cmd)
    assert 'openhab_db' in result


def test_user_priviliges_are_set(host):
    cmd = 'show grants for openhab'
    openhab_grant = execute_influx_command(host, cmd)
    assert 'openhab_db ALL PRIVILEGES' in openhab_grant
    cmd = 'show grants for grafana'
    grafana_grant = execute_influx_command(host, cmd)
    assert 'openhab_db READ' in grafana_grant


def test_influxdb_database_restored(host):
    cmd = 'show series'
    result = execute_influx_command(host, cmd)
    nlines = result.count('\n')
    assert nlines > 50

