"""Parse `show ip int brief` with regex — the two-pattern + zip recipe from Lesson 11."""
import os
import re

import netmiko

conn = netmiko.ConnectHandler(
    host=os.environ.get("PYNE_ROUTER_HOST", "10.254.0.1"),
    username=os.environ.get("PYNE_USERNAME", "cisco"),
    password=os.environ.get("PYNE_PASSWORD", "cisco"),
    device_type=os.environ.get("PYNE_DEVICE_TYPE", "cisco_ios"),
)
output = conn.send_command("show ip int brief")
conn.disconnect()

# Two regexes, one zip — straight from the lesson.
names = re.findall(r"^(GigabitEthernet\S+)", output, re.M)
states = re.findall(
    r"^GigabitEthernet\S+\s.*?(up|down|administratively down)\s*$",
    output,
    re.M,
)

for name, state in zip(names, states):
    print(f"{name:25s} {state}")
