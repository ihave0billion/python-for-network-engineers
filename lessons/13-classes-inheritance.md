# Lesson 13 — Classes, Methods, and Inheritance

## Class basics
```python
class Cisco:
    support = 'support@cisco.com'        # class variable

    def __init__(self, hostname, ip, ...):
        self.hostname = hostname         # instance variables
        ...

    def login(self):
        return netmiko.ConnectHandler(**self.conn_data)
```

`__init__` is the initializer; `self` references the instance.

## Inheritance
```python
class CiscoIOSRouter(CiscoIOSBase):
    def get_run(self):
        return self.conn.send_command('sh run')
```
Use `super().__init__(...)` to call the parent initializer.

## Lab
See `labs/13_classes/cisco.py`.