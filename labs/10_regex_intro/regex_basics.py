"""Regex basics on a chunk of Cisco config: search, findall, sub."""
import re

config = """
interface GigabitEthernet1/0/0
 ip address 10.0.0.1 255.255.255.0
 no shutdown
interface GigabitEthernet1/0/1
 ip address 10.0.1.1 255.255.255.0
 shutdown
"""

# search() — first match (returns Match or None)
m = re.search(r"ip address (\d+\.\d+\.\d+\.\d+)", config)
print(f"first ip:  {m.group(1)}")

# findall() — every match as a list of strings (or tuples if groups > 1)
ips = re.findall(r"ip address (\d+\.\d+\.\d+\.\d+)", config)
print(f"all ips:   {ips}")

# sub() — substitute (rename interface prefix for terser output)
shortened = re.sub(r"GigabitEthernet", "Gi", config).strip()
print()
print("after sub:")
print(shortened)
