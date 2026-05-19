"""Cisco router class with inheritance — instance method calls Netmiko."""
import os

import netmiko


class CiscoBase:
    """Common state shared across every Cisco device we'd manage."""

    support = "support@cisco.com"  # class variable — same for every instance

    def __init__(self, name, host, username, password, device_type):
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.device_type = device_type

    def login(self):
        return netmiko.ConnectHandler(
            host=self.host,
            username=self.username,
            password=self.password,
            device_type=self.device_type,
        )


class CiscoIOSRouter(CiscoBase):
    """An IOS-flavored router. Inherits __init__ + login from CiscoBase."""

    def get_version(self) -> str:
        with self.login() as conn:
            out = conn.send_command("show version | include Version")
        return out.splitlines()[0] if out else ""


router = CiscoIOSRouter(
    name=os.environ.get("PYNE_ROUTER_NAME", "R1"),
    host=os.environ.get("PYNE_ROUTER_HOST", "10.254.0.1"),
    username=os.environ.get("PYNE_USERNAME", "cisco"),
    password=os.environ.get("PYNE_PASSWORD", "cisco"),
    device_type=os.environ.get("PYNE_DEVICE_TYPE", "cisco_ios"),
)
print(f"{router.name}: {router.get_version()}")
