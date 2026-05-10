# Lesson 9 — Reading and Writing a JSON File

## Reading JSON
```python
import json
with open('file.json') as f:
    data = json.load(f)
```
`json.load` deserializes a file; `json.loads` deserializes a string.

JSON → Python: object→dict, array→list, string→str, number→int/float,
true/false→True/False, null→None.

## pprint
`from pprint import pprint` — readable nested output.

## Writing JSON
```python
with open('out.json', 'w') as f:
    json.dump(data, f, indent=4)
```
`json.dumps(data)` returns a JSON string.

## Lab
See `labs/09_json/`.