"""if/elif/else with comparison, logical, and membership operators."""

interfaces = [
    {"name": "Gi1/0", "status": "up", "protocol": "up"},
    {"name": "Gi1/1", "status": "down", "protocol": "down"},
    {"name": "Gi1/2", "status": "up", "protocol": "down"},
    {"name": "Gi1/3", "status": "administratively down", "protocol": "down"},
]

trunk_ports = {"Gi1/0", "Gi1/1"}

for iface in interfaces:
    name = iface["name"]
    status = iface["status"]
    protocol = iface["protocol"]
    is_trunk = name in trunk_ports  # membership operator

    if status == "up" and protocol == "up":
        kind = "trunk" if is_trunk else "access"
        print(f"{name}: healthy ({kind})")
    elif status == "administratively down":
        print(f"{name}: shut by admin")
    elif status == "up" and protocol == "down":
        print(f"{name}: layer-1 up, layer-2 down")
    else:
        print(f"{name}: down")
