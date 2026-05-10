"""Booleans and truthiness."""

interface_up = True
interface_admin_down = False

print("up:", interface_up, "admin_down:", interface_admin_down)
print("up and not admin_down:", interface_up and not interface_admin_down)

# Truthiness
for value in [0, 1, "", "R1", [], [1], None]:
    print(repr(value), "->", bool(value))