"""for, while, range, dict iteration — break and continue."""

routers = ["R1", "R2", "R3", "R4"]

# Basic for over a list
for r in routers:
    print(f"polling {r}...")
print()

# range — half-open: stop is exclusive
print("loopbacks via range:")
for i in range(1, 5):
    print(f"  192.168.1.{i}")
print()

# Iterating a dict with .items()
mgmt_ips = {"R1": "10.0.0.1", "R2": "10.0.0.2", "R3": "10.0.0.3"}
print("mgmt IPs:")
for name, ip in mgmt_ips.items():
    print(f"  {name} -> {ip}")
print()

# while with break + continue
i = 0
print("scanning interfaces:")
while True:
    if i >= len(routers):
        break
    name = routers[i]
    i += 1
    if name == "R3":
        print(f"  skip {name} (in maintenance)")
        continue
    print(f"  scanning {name}")
