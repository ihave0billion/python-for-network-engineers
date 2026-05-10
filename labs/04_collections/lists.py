"""Lists – ordered, mutable."""

interfaces = ["Gi1", "Gi2", "Gi3"]

interfaces.append("Gi4")
interfaces.insert(0, "Gi0")
interfaces.remove("Gi2")

print("All interfaces:", interfaces)
print("First:", interfaces[0])
print("Last :", interfaces[-1])
print("Slice:", interfaces[1:3])

for i, name in enumerate(interfaces):
    print(f"{i}: {name}")