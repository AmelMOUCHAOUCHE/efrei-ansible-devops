import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nginx_running_and_enabled(host):
    app_service = host.service("nginx")
    assert app_service.is_running
    assert app_service.is_enabled


def test_nginx_listening(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening


def test_mysql_running_and_enabled(host):
    mysql_service = host.service("mysql")
    assert mysql_service.is_running
    assert mysql_service.is_enabled


def test_nodejs_installed(host):
    node = host.command("node --version")
    assert node.rc == 0


def test_api_service_running(host):
    api_service = host.service("devops-api")
    assert api_service.is_running
    assert api_service.is_enabled


def test_api_listening(host):
    assert host.socket("tcp://0.0.0.0:3000").is_listening
