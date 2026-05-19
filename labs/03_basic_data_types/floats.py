"""Floats — note floating-point precision and round() fix."""
import netmiko

ip_base = '10.254.0.'
ip_end = 0.1


def get_ip_int_br(ip):
    conn = netmiko.ConnectHandler(
        ip=ip, username='cisco', password='cisco',
        device_type='cisco_ios',
    )
    return conn.send_command('show ip interface brief')


# 0.1 + 0.1 + 0.1 is 0.30000000000000004 in IEEE-754, so a naive
# `while ip_end <= 0.3` exits one iteration too early. Rounding to one
# decimal restores the behavior you'd expect from CLI math.
while round(ip_end, 1) <= 0.3:
    last_octet = int(round(ip_end * 10))
    ip = ip_base + str(last_octet)
    print(get_ip_int_br(ip))
    print('_' * 80)
    ip_end += 0.1