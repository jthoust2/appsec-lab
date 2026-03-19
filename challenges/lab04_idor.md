# Lab 04 — Insecure Direct Object Reference (IDOR)

**Points:** 15 | **Difficulty:** Intermediate

---

## Background

IDOR is the #1 vulnerability in the OWASP Top 10 (2021). It happens when an
application checks *authentication* (are you logged in?) but not *authorization*
(do you own this specific resource?). Any user can access any other user's data
just by changing an ID in the URL.

---

## Your task

Open `workspace/app.py` and ask **GitHub Copilot Chat** exactly this:

> *"Write a Flask GET /invoice/<invoice_id> route that returns the invoice
> as JSON for the logged-in user"*

Accept the code Copilot generates **without editing it first**.

---

## Questions (answer in `lab04_answers.md`)

**Q1.** Show the database query Copilot generated. Does it filter by the
current user's ID anywhere?

**Q2.** Describe step-by-step how an attacker who is logged in as User A
could read User B's invoices. What do they change in the request?

**Q3.** Why does returning HTTP `403 Forbidden` (instead of `404 Not Found`)
when a resource belongs to another user make things *worse* for security?

**Q4.** Fix the route so the query scopes results to the current user.
Paste your fixed version.

---

## Acceptance criteria

- [ ] `pytest tests/test_lab04.py -v` — all 3 tests pass
- [ ] User A cannot retrieve User B's invoice (cross-user test passes)
- [ ] `lab04_answers.md` contains answers to all 4 questions

---

## Hint (read only if stuck)

<details>
<summary>Reveal hint</summary>

The dangerous query:
```python
invoice = db.execute("SELECT * FROM invoices WHERE id = ?",
                     (invoice_id,)).fetchone()
```

The fix — scope to current user:
```python
invoice = db.execute(
    "SELECT * FROM invoices WHERE id = ? AND user_id = ?",
    (invoice_id, current_user_id)
).fetchone()
if not invoice:
    return {}, 404  # 404, not 403 — don't confirm existence
```

</details>
