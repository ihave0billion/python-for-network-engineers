# Lab 9 — Reading and Writing a JSON File

Run `python parse_device_json.py` to parse a JSON string with
`json.loads`, walk the nested structure (a list of interface dicts),
mutate it, and pretty-print the result with `json.dumps(..., indent=2)`.

## Expected output

```
device: R1
  Gi1/0  10.0.0.1/24   vlan 10
  Gi1/1  10.0.1.1/24   vlan 20

updated:
{
  "device": "R1",
  "interfaces": [
    {
      "name": "Gi1/0",
      "ip": "10.0.0.1/24",
      "vlan": 10
    },
    {
      "name": "Gi1/1",
      "ip": "10.0.1.1/24",
      "vlan": 20
    },
    {
      "name": "Gi1/2",
      "ip": "10.0.2.1/24",
      "vlan": 30
    }
  ]
}
```
