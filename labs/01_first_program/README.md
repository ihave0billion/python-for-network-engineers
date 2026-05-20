# Lab 1 — Execute Your First Python Program

## Goal
Use Netmiko to SSH into a Cisco router and print the output of
`show version` from a Python script.

## Prerequisites
- Python 3.10+ (`python3 --version`)
- A reachable IOS / IOS-XE / NX-OS device, or fall back to the recorded
  output described below.

## Steps
1. `cd labs/01_first_program`
2. `pip install netmiko`
3. Open `get_software_version.py` and replace `ip`, `username`, and
   `password` with values for your lab gear. Adjust `device_type` if you're
   targeting NX-OS (`cisco_nxos`) or IOS-XE (`cisco_xe`).
4. `python3 get_software_version.py`

You should see the full `show version` block print to your terminal.

## No router handy?
Skip the Netmiko run for now. The point of Lesson 1 is the *shape* of a
Python script: variables at the top, action at the bottom. You'll revisit
this same code with deeper context in Lessons 12–14 (functions, modules)
and again when we cover Netmiko proper.

## What to notice
- `import netmiko` pulls in a third-party library that wraps SSH +
  Cisco-aware prompts/paging so you don't have to.
- The seven variables at the top are the script's *data model*. Swap them
  out and the same code targets a different device.
- `conn.send_command(...)` returns the router's stdout as a Python string.
  That string is the on-ramp to every parsing and validation pattern you'll
  meet later in the course.
