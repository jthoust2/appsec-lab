# Lab 03 — Broken Authentication (Weak Password Hashing)

**Points:** 15 | **Difficulty:** Beginner–Intermediate

---

## Background

Not all hash functions are equal. MD5 and SHA-1 were designed for *speed*
(checksums, file integrity). That speed is catastrophic for passwords:
a modern GPU can compute **10 billion MD5 hashes per second**, cracking
most passwords in seconds. Password hashing requires deliberate *slowness*
and a unique *salt* per user.

---

## Your task

Open `workspace/app.py` and ask **GitHub Copilot Chat** exactly this:

> *"Write a register_user(username, password) function that hashes the
> password and stores the user in the SQLite database"*

Accept the code Copilot generates **without editing it first**.

---

## Questions (answer in `lab03_answers.md`)

**Q1.** What hashing algorithm did Copilot use? Is it salted?

**Q2.** The MD5 hash of the password `password` is
`5f4dcc3b5aa765d61d8327deb882cf99`.
Why does this make a database breach catastrophic even without the
attacker cracking anything?

**Q3.** If two users both choose `password` as their password and you use
MD5 without a salt, what do their stored hashes look like? What does this
reveal to an attacker?

**Q4.** Fix the function to use **bcrypt** with `rounds=12`. Paste your
fixed version including a matching `verify_login()` function.

**Q5.** Why does bcrypt take ~250ms per hash? Is that a bug or a feature?

---

## Acceptance criteria

- [ ] `pytest tests/test_lab03.py -v` — all 3 tests pass
- [ ] `bandit -r workspace/ -ll` reports no use of MD5/SHA1 for passwords
- [ ] `lab03_answers.md` contains answers to all 5 questions

---

## Hint (read only if stuck)

<details>
<summary>Reveal hint</summary>

The dangerous pattern:
```python
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()
```

The fix:
```python
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Verification:
bcrypt.checkpw(password.encode(), stored_hash)
```

</details>
