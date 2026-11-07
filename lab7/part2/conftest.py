import pytest
import paramiko
import subprocess

server_ip = "server_ip" 
username = "username"
password = "password"

@pytest.fixture(scope='function')
def server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname=server_ip, username=username, password=password)
    stdin, stdout, stderr = client.exec_command('iperf -s -D')
    error = stderr.read().decode()

    yield error

    client.close()

@pytest.fixture(scope='function')
def client(server):
    command = ["iperf", "-c", server_ip, "-i", "1"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = process.communicate(timeout=15)

    return out, err

