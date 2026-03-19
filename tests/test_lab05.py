"""
tests/test_lab05.py — Sensitive Data Exposure tests
"""
import ast
import os
import re


LAB_FILE = os.path.join(os.path.dirname(__file__), '..', 'workspace', 'app.py')

KNOWN_SECRET_PATTERNS = [
    r'AKIA[0-9A-Z]{16}',          # AWS access key
    r'sk_live_[a-zA-Z0-9]{24,}',  # Stripe live key
    r'sk_test_[a-zA-Z0-9]{24,}',  # Stripe test key
    r'ghp_[a-zA-Z0-9]{36}',       # GitHub personal token
]

WEAK_ASSIGNMENTS = [
    r'(API_KEY|SECRET|PASSWORD|TOKEN|PASSWD|PWD)\s*=\s*["\'][^"\']{4,}["\']',
]


def read_source():
    with open(LAB_FILE) as f:
        return f.read()


def test_no_hardcoded_aws_keys():
    """AWS access key pattern must not appear as a literal string."""
    source = read_source()
    for pattern in KNOWN_SECRET_PATTERNS[:1]:
        assert not re.search(pattern, source), (
            "Hardcoded AWS key found in source! Use os.environ[] instead."
        )


def test_no_hardcoded_stripe_keys():
    """Stripe key pattern must not appear as a literal string."""
    source = read_source()
    for pattern in KNOWN_SECRET_PATTERNS[1:3]:
        assert not re.search(pattern, source), (
            "Hardcoded Stripe key found in source! Use os.environ[] instead."
        )


def test_uses_os_environ():
    """Code must reference os.environ to load at least one secret."""
    source = read_source()
    assert "os.environ" in source or "os.getenv" in source, (
        "No os.environ[] calls found. "
        "Load secrets from environment variables, not hardcoded strings."
    )
