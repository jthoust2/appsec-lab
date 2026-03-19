"""
tests/test_lab04.py — IDOR tests
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'workspace'))


@pytest.fixture(autouse=True)
def seed_invoices(app):
    import app as student_app
    with app.app_context():
        db = student_app.get_db()
        db.execute("DELETE FROM invoices")
        db.execute("INSERT INTO invoices (id,user_id,amount,details) VALUES (1,'alice',100,'Invoice A')")
        db.execute("INSERT INTO invoices (id,user_id,amount,details) VALUES (2,'bob',200,'Invoice B')")
        db.commit()


def test_owner_can_access_invoice(client, app):
    """User alice can access her own invoice."""
    import app as student_app
    with client.session_transaction() as sess:
        sess["user_id"] = "alice"
    r = client.get("/invoice/1")
    assert r.status_code == 200, "Owner should be able to access their invoice"


def test_nonowner_cannot_access_invoice(client, app):
    """User alice must NOT be able to access bob's invoice."""
    with client.session_transaction() as sess:
        sess["user_id"] = "alice"
    r = client.get("/invoice/2")
    assert r.status_code in (403, 404), (
        "IDOR vulnerability: alice accessed bob's invoice! "
        "Add user_id = ? filter to your query."
    )


def test_unauthenticated_returns_401(client):
    """Unauthenticated requests must return 401."""
    r = client.get("/invoice/1")
    assert r.status_code == 401, "Unauthenticated request should return 401"
