"""
tests/test_lab03.py — Broken Authentication tests
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'workspace'))


def test_register_does_not_store_plaintext(app):
    """Password must not be stored as plaintext."""
    import app as student_app
    with app.app_context():
        student_app.register_user("testuser_lab03", "mypassword")
        db = student_app.get_db()
        row = db.execute(
            "SELECT password FROM users WHERE username=?",
            ("testuser_lab03",)
        ).fetchone()
        assert row is not None, "User was not stored in the database"
        stored = row[0] if isinstance(row, tuple) else row["password"]
        assert stored != "mypassword", "Password stored as plaintext!"
        assert "mypassword" not in str(stored), "Password visible in stored hash"


def test_register_does_not_use_md5(app):
    """MD5 hash of 'test' must not appear in stored value."""
    import app as student_app
    import hashlib
    md5_of_test = hashlib.md5(b"testpw").hexdigest()
    with app.app_context():
        student_app.register_user("testuser_md5", "testpw")
        db = student_app.get_db()
        row = db.execute(
            "SELECT password FROM users WHERE username=?",
            ("testuser_md5",)
        ).fetchone()
        stored = row[0] if isinstance(row, tuple) else row["password"]
        assert md5_of_test not in str(stored), (
            "MD5 hash detected! Use bcrypt, scrypt, or Argon2 instead."
        )


def test_bcrypt_verify_works(app):
    """verify_login() must return True for correct password."""
    import app as student_app
    with app.app_context():
        student_app.register_user("testuser_verify", "correcthorsebattery")
        result = student_app.verify_login("testuser_verify", "correcthorsebattery")
        assert result is True, "verify_login() returned False for correct password"
