# Lesson 19 — Python pdb

## Three ways to invoke
- Script:    `python -m pdb script.py`
- REPL:      `import pdb; pdb.run('script.py')`
- In code:   `breakpoint()` (3.7+) or `import pdb; pdb.set_trace()`

## Common commands
| Command | Action |
| --- | --- |
| `c` continue | Run until next breakpoint or end |
| `s` step    | Step into function |
| `n` next    | Step over function |
| `b N`       | Set breakpoint at line N |
| `p var`     | Print var |
| `pp var`    | Pretty-print |
| `! stmt`    | Execute Python statement |
| `l`         | List source |
| `w`         | Where (stack) |
| `q`         | Quit |

## Lab
See `labs/19_pdb/cisco_restconf.py`.