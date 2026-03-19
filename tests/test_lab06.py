"""
tests/test_lab06.py — Command Injection tests
"""


def test_valid_hostname_returns_200(client):
    """A valid hostname should be accepted."""
    r = client.post("/ping", data={"hostname": "8.8.8.8"})
    assert r.status_code == 200, "Valid hostname should return 200"


def test_semicolon_payload_rejected(client):
    """Semicolon injection payload must be rejected with 400."""
    r = client.post("/ping", data={"hostname": "8.8.8.8; cat /etc/passwd"})
    assert r.status_code == 400, (
        "Command injection not blocked: semicolon payload was accepted. "
        "Add input validation with a hostname allowlist regex."
    )


def test_subshell_payload_rejected(client):
    """Subshell $() payload must be rejected with 400."""
    r = client.post("/ping", data={"hostname": "$(id)"})
    assert r.status_code == 400, (
        "Command injection not blocked: $() payload was accepted. "
        "Only allow [a-zA-Z0-9.-] characters in hostname input."
    )
