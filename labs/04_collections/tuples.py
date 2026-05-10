"""Tuples – ordered, immutable."""

loopback = ("10.0.0.1", "255.255.255.255")
ip, mask = loopback   # unpacking

print("IP  :", ip)
print("Mask:", mask)

# Tuples can be dict keys (lists cannot)
links = {
    ("R1", "R2"): "GigabitEthernet0/0/0",
    ("R1", "R3"): "GigabitEthernet0/0/1",
}
for endpoints, iface in links.items():
    print(endpoints, "->", iface)
    
    