"""json.loads to read, json.dumps to write — pretty-print with indent=2."""
import json

raw = """
{
  "device": "R1",
  "interfaces": [
    {"name": "Gi1/0", "ip": "10.0.0.1/24", "vlan": 10},
    {"name": "Gi1/1", "ip": "10.0.1.1/24", "vlan": 20}
  ]
}
"""

data = json.loads(raw)
print(f"device: {data['device']}")
for iface in data["interfaces"]:
    print(f"  {iface['name']:6s} {iface['ip']:13s} vlan {iface['vlan']}")

# Mutate the structure and dump it back out as a JSON string.
data["interfaces"].append({"name": "Gi1/2", "ip": "10.0.2.1/24", "vlan": 30})
print()
print("updated:")
print(json.dumps(data, indent=2))
