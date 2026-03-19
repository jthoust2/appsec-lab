"""
tests/test_lab01.py — SQL Injection tests
"""
import pytest
import bcrypt


@pytest.fixture(autouse=True)
def seed_user(app):
    """Insert a test user before each test."""
    import app as student_app
    with app.app_context():
        db = student_app.get_db()
        hashed = bcrypt.hashpw(b"correct-password", bcrypt.gensalt())
        db.execute("DELETE FROM users WHERE username='alice'")
        db.execute("INSERT INTO users VALUES (?,?)", ("alice", hashed))
        db.commit()


def test_valid_login_succeeds(client):
    """Correct credentials return 200."""
    r = client.post("/login", data={
        "username": "alice",
        "password": "correct-password"
    })
    assert r.status_code == 200, "Valid login should return 200"


def test_wrong_password_fails(client):
    """Wrong password returns 401."""
    r = client.post("/login", data={
        "username": "alice",
        "password": "wrongpassword"
    })
    assert r.status_code == 401, "Wrong password should return 401"


def test_sqli_bypass_fails(client):
    """Classic SQLi bypass ' OR '1'='1 must NOT succeed."""
    r = client.post("/login", data={
        "username": "' OR '1'='1",
        "password": "anything"
    })
    assert r.status_code == 401, (
        "SQL injection bypass succeeded! "
        "Fix your query to use parameterized statements."
    )
