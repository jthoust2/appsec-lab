# Lab 07 — XML External Entity (XXE) Injection

**Points:** 10 | **Difficulty:** Intermediate–Advanced

---

## Background

XXE occurs when an XML parser processes external entity references in
user-supplied XML. An attacker can define an entity that reads a local
file (e.g., `/etc/passwd`, cloud credentials) and have the server return
its contents. The same technique can trigger Server-Side Request Forgery
(SSRF) to scan internal networks.

---

## Your task

Open `workspace/app.py` and ask **GitHub Copilot Chat** exactly this:

> *"Write a Flask POST /upload route that accepts an XML file upload
> and returns the parsed content as JSON"*

Accept the code Copilot generates **without editing it first**.

---

## Questions (answer in `lab07_answers.md`)

**Q1.** What XML parser and settings did Copilot use?
Are external entities enabled or disabled by default?

**Q2.** Write the malicious XML payload that would make the server read
and return the contents of `/etc/passwd`. Include the full DOCTYPE
declaration.

**Q3.** Besides local file disclosure, name one other attack that XXE enables.
Describe how it works in one sentence.

**Q4.** Fix the route using the `defusedxml` library.
Paste your fixed version.

**Q5.** If you must use `lxml` directly, what three parser arguments
disable external entity processing?

---

## Acceptance criteria

- [ ] `pytest tests/test_lab07.py -v` — all 3 tests pass
- [ ] The malicious XXE payload returns a 400 error, not file contents
- [ ] `lab07_answers.md` contains answers to all 5 questions

---

## Hint (read only if stuck)

<details>
<summary>Reveal hint</summary>

The dangerous pattern:
```python
from lxml import etree
parser = etree.XMLParser()   # external entities ON by default
tree = etree.fromstring(xml_data, parser)
```

Malicious payload:
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<data>&xxe;</data>
```

The fix:
```python
from defusedxml import ElementTree
tree = ElementTree.fromstring(xml_data)   # safe by default
```

Or with lxml explicitly:
```python
parser = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    dtd_validation=False
)
```

</details>
