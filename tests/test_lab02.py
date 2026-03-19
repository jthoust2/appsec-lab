"""
tests/test_lab02.py — XSS tests
"""


def test_normal_search_returns_200(client):
    """Normal query renders a response."""
    r = client.get("/search?q=hello")
    assert r.status_code == 200


def test_script_tag_is_escaped(client):
    """<script> in query must appear as escaped text, not raw HTML."""
    payload = "<script>alert('xss')</script>"
    r = client.get(f"/search?q={payload}")
    data = r.data.decode()
    assert "<script>" not in data, (
        "XSS vulnerability: <script> tag was rendered as raw HTML. "
        "Use markupsafe.escape() or equivalent on the query parameter."
    )
    # The escaped version should appear as visible text
    assert "&lt;script&gt;" in data or "alert" not in data


def test_img_onerror_is_escaped(client):
    """<img onerror=...> payload must not execute."""
    payload = "<img src=x onerror=alert(1)>"
    r = client.get(f"/search?q={payload}")
    data = r.data.decode()
    assert "<img" not in data or "onerror" not in data, (
        "XSS vulnerability: <img onerror=...> was not escaped. "
        "Ensure all HTML special characters are encoded."
    )
