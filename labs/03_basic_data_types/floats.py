"""Floats — note floating-point precision and round() fix."""
import netmiko

ip_base = '10.254.'
ip_end = 0.1


def get_ip_int_br(ip):
    conn = netmiko.ConnectHandler(
        ip=ip, username='cisco', password='cisco',
        device_type='cisco_ios',
    )
    return conn.send_command('show ip interface brief')


while ip_end <= 0.3:
    ip = ip_base + '0.' + str(int(ip_end * 10))e