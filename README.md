# AppSec Vibe Coding Lab

> **Application Security Course — GitHub Copilot Security Challenge**

In this lab you will use GitHub Copilot to generate code, then identify
and fix the security vulnerabilities it introduces. Every lab follows the
same loop:

1. Read the challenge card in `challenges/`
2. Ask Copilot the exact prompt given
3. Accept the generated code without editing it first
4. Identify the vulnerability and write your exploit in `labXX_answers.md`
5. Fix the code
6. Run the tests — push until you get a green tick

---

## Setup

```bash
# 1. Fork this repo on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/appsec-lab
cd appsec-lab

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install flask bcrypt defusedxml bandit pytest semgrep python-dotenv markupsafe

# 4. Open in VS Code — accept the extension recommendations when prompted
code .
```

GitHub Copilot must be signed in. If not: `Ctrl+Shift+P` →
*GitHub Copilot: Sign In*.

---

## Lab challenges

| Lab | Vulnerability | Challenge card | Points |
|-----|--------------|----------------|--------|
| 01 | SQL Injection | [lab01_sqli.md](challenges/lab01_sqli.md) | 15 |
| 02 | Cross-Site Scripting | [lab02_xss.md](challenges/lab02_xss.md) | 15 |
| 03 | Broken Authentication | [lab03_auth.md](challenges/lab03_auth.md) | 15 |
| 04 | IDOR | [lab04_idor.md](challenges/lab04_idor.md) | 15 |
| 05 | Sensitive Data Exposure | [lab05_secrets.md](challenges/lab05_secrets.md) | 15 |
| 06 | Command Injection | [lab06_cmdi.md](challenges/lab06_cmdi.md) | 15 |
| 07 | XXE Injection | [lab07_xxe.md](challenges/lab07_xxe.md) | 10 |

**Total: 100 points**

All your code goes in `workspace/app.py`. Each lab section is clearly marked.

---

## Running tests locally

```bash
# Run all tests
pytest tests/ -v

# Run one lab at a time
pytest tests/test_lab01.py -v

# Run the security scanner
bandit -r workspace/ -ll
```

---

## Submitting

1. Push your changes to your fork
2. Open a **Pull Request** — GitHub Actions runs the grader automatically
3. A green tick = all tests pass — submit the PR URL to Canvas
4. A red X = read the test output, fix the issue, and push again

---

## Rules

- You **must** use Copilot to generate the initial vulnerable code
- Do **not** look at the `solutions/` folder until after you submit
- You may push as many times as you like before the deadline
- Collaboration on understanding vulnerabilities is encouraged;
  sharing fixed code is not
