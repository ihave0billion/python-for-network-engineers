# GitHub Setup — `prne` (Python for Network Engineers app)

This guide walks through publishing this project to a **public** GitHub repository
under your personal account. Run the commands in order. Stop at each checkpoint
and confirm before continuing.

> The project is public from day one. Never commit real router IPs, usernames,
> or passwords. Anything sensitive lives in `config.yaml` / `.env`, both
> gitignored. Only the `*.example` templates get pushed.

---

## 0. Prerequisites

- Git installed: `git --version`
- GitHub CLI installed (recommended): `gh --version`
  - Install on macOS: `brew install gh`
- Authenticated to GitHub: `gh auth status`
  - If not authenticated: `gh auth login` and follow the browser prompt

---

## 1. Pick a repo name and identity

Suggested name: **`prne-python-for-network-engineers`** (or shorter: `prne`).

Set your local git identity (only needed once per machine):

```bash
git config --global user.name  "Your Name"
git config --global user.email "21garcia21@gmail.com"
```

---

## 2. Initialize the local repo

From the project root:

```bash
cd "/Users/hectgarc/Library/CloudStorage/OneDrive-Cisco/Documents/Development/claude-code-python-neteng-app"
git init -b main
```

`-b main` sets the default branch name to `main` (not `master`).

---

## 3. Verify hygiene files exist before the first commit

These files must exist and have correct content **before** you commit:

| File | Purpose |
|---|---|
| `.gitignore` | Excludes `config.yaml`, `.env`, `__pycache__/`, `.venv/`, `~/.prne/`, OS files |
| `LICENSE` | MIT license (public repo needs one) |
| `README.md` | Project overview, install, quickstart |
| `config.example.yaml` | Template for router config — safe to commit |
| `.env.example` | Template for env vars — safe to commit |

Sanity check — these should print **nothing** (no real secrets staged):

```bash
git status
grep -RIn --include='*.yaml' --include='*.env' -E '10\.254\.|password.*cisco' . || echo "clean"
```

If `grep` finds matches, move those values into `config.yaml` / `.env` (gitignored)
before continuing.

---

## 4. First commit

```bash
git add .gitignore LICENSE README.md GITHUB_SETUP.md \
        config.example.yaml .env.example \
        pyproject.toml \
        lessons/ labs/ checks/ prne/ \
        teach-me-python.md "Python for Network Engineer notes.pdf"
git status                      # review what's staged
git commit -m "Initial commit: PRNE app scaffolding and existing course materials"
```

> Use `git add <paths>` (above), not `git add -A` — that would catch any stray
> `config.yaml` or `.env` you forgot to gitignore.

---

## 5. Create the GitHub repo and push

Using the GitHub CLI (one command for create + push):

```bash
gh repo create prne-python-for-network-engineers \
  --public \
  --source=. \
  --remote=origin \
  --description "Interactive Python course for Cisco network engineers" \
  --push
```

If you prefer the web UI:

1. Go to <https://github.com/new>
2. Owner: your personal account · Name: `prne-python-for-network-engineers` · Public
3. **Do NOT** initialize with README/license/gitignore (we already have them)
4. Copy the SSH or HTTPS URL it shows, then:

```bash
git remote add origin git@github.com:<your-username>/prne-python-for-network-engineers.git
git push -u origin main
```

---

## 6. Verify on GitHub

```bash
gh repo view --web        # opens the repo in your browser
```

Confirm:
- README renders
- LICENSE is detected (look for "MIT" in the sidebar)
- No `config.yaml` or `.env` file is visible

---

## Day-to-day git workflow

After this, the loop for every change is:

```bash
git status                                    # see what changed
git diff                                      # review unstaged changes
git add <files>                               # stage specific files
git commit -m "Short, present-tense message"  # commit
git push                                      # push to origin/main
```

For larger changes, use a feature branch:

```bash
git checkout -b feat/lab-runner
# ... make changes, commit ...
git push -u origin feat/lab-runner
gh pr create --fill                           # opens a PR
```

---

## Branch / commit message conventions

- Branch names: `feat/<thing>`, `fix/<thing>`, `docs/<thing>`
- Commit subject: imperative mood, ≤ 60 chars (e.g. "Add lab runner fallback")
- Body (optional): why, not what — the diff shows what

---

## Safety reminders

- **Never** force-push to `main` (`git push --force` on a shared branch). Use a new branch instead.
- **Never** commit `config.yaml`, `.env`, `*.pem`, or anything under `~/.prne/`.
- If you accidentally commit a secret: rotate the credential first, then remove from history (`git filter-repo` or BFG). Force-push is acceptable here, and only here.
- Public repo means anyone can read history. Treat every push as permanent.
