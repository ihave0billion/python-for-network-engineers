# Lesson 1 — Your First Python Program

## Install Python
You need Python 3.10 or newer. Check what's already on the box:

```
python3 --version
```

If it's missing or too old:

| OS | Install command |
|---|---|
| macOS | `brew install python` (after installing Homebrew from brew.sh) |
| Debian / Ubuntu | `sudo apt install python3 python3-pip` |
| RHEL / Rocky | `sudo dnf install python3 python3-pip` |
| Windows | Download from python.org and tick **Add Python to PATH** in the installer |

## Running a script
A Python program is a plain text file ending in `.py`. Hand it to the
interpreter:

```
python3 hello.py
```

That's it. No compile step, no `main()`, no semicolons. Two lines is a real
program:

```python
greeting = "Hello, Network!"
print(greeting)
```

`greeting` is a *variable* — a name bound to a value. `print()` is a built-in
function that writes to stdout. Save those two lines as `hello.py` and run
them.

## Your first network script
Now look at `labs/01_first_program/get_software_version.py`:

```python
import netmiko

ip = '10.254.0.1'
username = 'cisco'
password = 'cisco'
device_type = 'cisco_ios'
port = 22

conn = netmiko.ConnectHandler(
    ip=ip, username=username, password=password,
    device_type=device_type, port=port,
)
print(conn.send_command('show version'))
```

You don't need to understand every line yet — read the shape. Variables at
the top hold the *data* (IP, credentials, platform). Code at the bottom
*acts* on that data. The router's `show version` output comes back as a
Python string you can store, parse, diff, or log.

Five lines of CLI on one box becomes one Python script you can point at 300.
That's the CLI-to-data shift in concrete form.

## Lab
See `labs/01_first_program/`. `pip install netmiko`, edit the IP/credentials
to match your lab gear, then `python3 get_software_version.py`. No router
today? The two-line Hello, Network above is enough — every later lesson
builds on it.
