# Lab 05 — Sensitive Data Exposure (Hardcoded Secrets)

**Points:** 15 | **Difficulty:** Beginner

---

## Background

Secrets hardcoded in source code are exposed the moment code is shared,
committed to GitHub, or accessed by any team member. GitHub scans public
repos for known secret patterns and notifies attackers within minutes.
Even after deletion, secrets persist in git history forever.

---

## Your task

Open `workspace/app.py` and ask **GitHub Copilot Chat** exactly this:

> *"Write a Python module that connects to AWS S3 and a Stripe payment API
> using configuration variables at the top of the file"*

Accept the code Copilot generates **without editing it first**.

---

## Questions (answer in `lab05_answers.md`)

**Q1.** List every secret Copilot hardcoded. What type is each one
(AWS key, DB password, API key, etc.)?

**Q2.** If this file was accidentally pushed to a public GitHub repo and
deleted 5 minutes later, is the secret safe? Explain why or why not.

**Q3.** How would an attacker find leaked AWS keys on GitHub automatically?
Name one tool or technique.

**Q4.** Fix the code using `python-dotenv` and environment variables.
Paste your fixed version AND a sample `.env` file (with fake values).

**Q5.** What file must always be in `.gitignore` to prevent the `.env`
file from being committed?

---

## Acceptance criteria

- [ ] `pytest tests/test_lab05.py -v` — all 3 tests pass
- [ ] `trufflehog filesystem workspace/` finds no secrets
- [ ] No string matching `AKIA`, `sk_live_`, or `password` appears as a
  literal value in `workspace/app.py`
- [ ] `lab05_answers.md` contains answers to all 5 questions

---

## Hint (read only if stuck)

<details>
<summary>Reveal hint</summary>

The dangerous pattern:
```python
AWS_KEY    = "AKIAIOSFODNN7EXAMPLE"
STRIPE_KEY = "sk_live_abc123"
```

The fix:
```python
import os
from dotenv import load_dotenv
load_dotenv()

AWS_KEY    = os.environ["AWS_ACCESS_KEY_ID"]
STRIPE_KEY = os.environ["STRIPE_SECRET_KEY"]
```

`.env` file (add to `.gitignore`!):
```
AWS_ACCESS_KEY_ID=your-key-here
STRIPE_SECRET_KEY=your-key-here
```

</details>
