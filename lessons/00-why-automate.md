# Lesson 0 — Why Automate? (CLI vs Data Mindset)

## The CLI bottleneck
Configuring 300 routers by hand takes 300 SSH sessions, 300 chances to typo,
and zero ways to audit what changed. The CLI is a *one-device interface*.
Modern networks are *systems*.

## The shift

| CLI thinking | Data thinking |
|---|---|
| `interface Gi0/1` → `description WAN` | `{"interface": "Gi0/1", "description": "WAN"}` |
| Run command on each box | Send the same data to N boxes |
| Output is text to read | Output is data to parse |
| State lives in the device | State lives in your repo |

## What "data-oriented" gets you
- **Repeatable** — one script touches 300 routers identically.
- **Auditable** — `git diff` shows what changed and who changed it.
- **Composable** — pipelines, validators, dashboards built on the same data.
- **Reviewable** — your peers can read intent before it hits the box.

## The hidden trade
You stop typing commands and start writing code. Python is the lingua franca
that gets you there. The rest of this course teaches you Python *as a
network engineer would learn it* — every concept backed by a Cisco example.

## Lab
None for this lesson. Press **m** to mark complete, then **n** for Lesson 1.
