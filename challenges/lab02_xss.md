# Lab 02 — Cross-Site Scripting (XSS)

**Points:** 15 | **Difficulty:** Beginner

---

## Background

XSS occurs when user-supplied data is rendered as raw HTML in a browser response.
An attacker can inject a `<script>` tag that executes in any victim's browser who
clicks a crafted link — stealing cookies, hijacking sessions, or redirecting users.

---

## Your task

Open `workspace/app.py` and ask **GitHub Copilot Chat** exactly this:

> *"Write a Flask GET /search route that displays search results for a
> query parameter q in an HTML response"*

Accept the code Copilot generates **without editing it first**.

---

## Questions (answer in `lab02_answers.md`)

**Q1.** Show the exact line in Copilot's code where user input enters the HTML.

**Q2.** Write a URL an attacker could send to a victim that would pop up an
alert box with the text `hacked`. (Use `<script>alert('hacked')</script>`)

**Q3.** What would a *real* attacker do instead of showing an alert?
Give one concrete example involving `document.cookie`.

**Q4.** Fix the route using the `escape-html` equivalent for Python
(`markupsafe.escape` is built into Flask). Paste your fixed version.

**Q5.** Name one additional HTTP header that would block this attack even
if the escaping was accidentally missed.

---

## Acceptance criteria

- [ ] `pytest tests/test_lab02.py -v` — all 3 tests pass
- [ ] `<script>` in the query parameter renders as visible text, not executed code
- [ ] `lab02_answers.md` contains answers to all 5 questions

---

## Hint (read only if stuck)

<details>
<summary>Reveal hint</summary>

The dangerous pattern:
```python
return f"<h2>Results for: {query}</h2>"
```

The fix using Flask's built-in escaping:
```python
from markupsafe import escape
return f"<h2>Results for: {escape(query)}</h2>"
```

The protective header:
```
Content-Security-Policy: default-src 'self'; script-src 'self'
```

</details>
