"""Get the running IOS version of a Cisco router via SSH."""
import netmiko

ip = '10.254.0.1'
username = 'cisco'
password = 'cisco'
device_type = 'cisco_ios'
port = 22

conn = netmiko.ConnectHandler(
    ip=ip, username=username, password=password,
    device_type=device_type, port=port,
)
print(conn.send_command('show version'))