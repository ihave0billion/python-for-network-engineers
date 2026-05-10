# Lesson 1 — Introducing Programming and Python for Network Engineers

## Programmability
Traditional CLI/SNMP-based network management does not scale. Network
programmability uses tools and APIs to deploy, manage and troubleshoot devices,
saving time, reducing human error, and providing greater control.

- **Automation**: repeatable tasks without human intervention
- **Orchestration**: combining tasks into a workflow

APIs evolved from vendor-specific (NX-API) to open (NETCONF, RESTCONF) to
controller-based (DNA Center, APIC) using northbound/southbound APIs.

### REST principles
Six constraints: Client/Server, Stateless, Cache, Uniform Interface, Layered
System, Code on Demand. REST uses HTTP methods (GET, POST, PUT, DELETE) and
returns status codes (2xx OK, 4xx client error, 5xx server error).

## Continued Importance of the CLI
The CLI is still required for advanced troubleshooting, older devices, console
access, and tools that lack API support.

## Need for Python
Python is interpretive, platform-flexible, object-oriented, open-source, and
has a huge ecosystem. Use Python 3.x. PEP documents drive the language;
PEP 8 (style) and PEP 20 (Zen of Python) are key.

## First Python Program
A library is reusable code (e.g. `netmiko`). A variable holds a value.
A simple `show version` script imports `netmiko`, defines connection
variables, opens an SSH connection, sends `show version`, and prints output.

## Lab
See `labs/01_first_program/` for an executable `get_software_version.py`.