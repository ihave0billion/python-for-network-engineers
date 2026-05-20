"""String operations — strip, split, slicing, case, f-string, count, startswith."""

hostname = "  csr1kv1.lab.local  "
ip = "10.254.0.7"

clean = hostname.strip()
short = clean.split(".")[0]
last_octet = ip.split(".")[-1]

print(f"short:      {short}")
print(f"last octet: {last_octet}")
print(f"upper:      {short.upper()}")

desc = "GigabitEthernet1/0/0 is up, line protocol is up"
print(f"'up' count: {desc.count('up')}")
print(f"prefix Gi?  {desc.startswith('Gigabit')}")
