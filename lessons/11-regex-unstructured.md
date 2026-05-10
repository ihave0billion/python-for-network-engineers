# Lesson 11 — Reading Raw or Unstructured Data Using Regular Expressions

When Netmiko returns CLI output, it's a raw string. Use regex to extract
fields, or use **TextFSM** with `use_textfsm=True` to get structured data
parsed by `ntc-templates`.

## Pattern → dict via zip
```python
ints = re.findall(r'(GigabitEthernet[1-9])\s', output)
stats = re.findall(r'GigabitEthernet[1-9].*(up|administratively down|down)',
                   output)
data = dict(zip(ints, stats))
```

## TextFSM
```python
out = csr.send_command("show ip int brief", use_textfsm=True)
```
TextFSM templates have **Value** definitions and a **Start** state with
regex rules; `Record` writes a row when matched.

## Lab
See `labs/11_regex_unstructured/edit_cisco_config.py`.