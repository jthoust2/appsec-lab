"""
conftest.py — shared fixtures for all AppSec lab tests
"""
import pytest
import sqlite3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'workspace'))


@pytest.fixture
def app():
    """Create a test Flask app with an in-memory database."""
    import app as student_app
    student_app.app.config["TESTING"] = True
    student_app.app.config["DATABASE"] = ":memory:"
    with student_app.app.app_context():
        student_app.init_db()
    return student_app.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    import app as student_app
    with app.app_context():
        conn = student_app.get_db()
        yield conn
