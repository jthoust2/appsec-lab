# Lab 06 — Command Injection

**Points:** 15 | **Difficulty:** Intermediate

---

## Background

Command injection occurs when user input is passed to a system shell
without sanitization. Shell metacharacters like `;`, `&&`, `|`, and `$()`
let an attacker append arbitrary OS commands that run with the same
privileges as the web server — often leading to full server compromise.

---

## Your task

Open `workspace/app.py` and ask **GitHub Copilot Chat** exactly this:

> *"Write a Flask POST /ping route that pings a hostname submitted by
> the user and returns the ping output"*

Accept the code Copilot generates **without editing it first**.

---

## Questions (answer in `lab06_answers.md`)

**Q1.** Show the exact `subprocess` call Copilot generated.
What argument makes it dangerous?

**Q2.** Write two different attacker payloads for the `hostname` field.
For each, show what OS command actually runs on the server:
- Payload that reads `/etc/passwd`
- Payload that creates a file called `pwned.txt`

**Q3.** Why does passing arguments as a **list** (instead of a string)
prevent command injection even without input validation?

**Q4.** Fix the route using two layers of defense:
  1. Input validation with a regex allowlist
  2. `shell=False` with arguments as a list

Paste your fixed version.

---

## Acceptance criteria

- [ ] `pytest tests/test_lab06.py -v` — all 3 tests pass
- [ ] Input `8.8.8.8; cat /etc/passwd` is rejected with a 400 error
- [ ] `bandit -r workspace/ -ll` reports no `subprocess_popen_with_shell_equals_true`
- [ ] `lab06_answers.md` contains answers to all 4 questions

---

## Hint (read only if stuck)

<details>
<summary>Reveal hint</summary>

The dangerous pattern:
```python
result = subprocess.run(f"ping -c 4 {hostname}",
                        shell=True, capture_output=True, text=True)
```

The fix:
```python
import re
if not re.match(r'^[a-zA-Z0-9.\-]{1,253}$', hostname):
    return {"error": "Invalid hostname"}, 400

result = subprocess.run(["ping", "-c", "4", hostname],
                        shell=False, capture_output=True, text=True)
```

</details>
