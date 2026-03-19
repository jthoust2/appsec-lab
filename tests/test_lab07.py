"""
tests/test_lab07.py — XXE Injection tests
"""


SAFE_XML = b"""<?xml version="1.0"?>
<inventory>
  <item><n>Widget</n><qty>10</qty></item>
</inventory>"""

XXE_PAYLOAD = b"""<?xml version="1.0"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<data>&xxe;</data>"""

BILLION_LAUGHS = b"""<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
]>
<root>&lol2;</root>"""


def test_valid_xml_returns_200(client):
    """Valid XML upload should return 200."""
    r = client.post("/upload", data={"file": (SAFE_XML, "data.xml")},
                    content_type="multipart/form-data")
    assert r.status_code == 200, "Valid XML should be accepted"


def test_xxe_payload_blocked(client):
    """XXE payload with external entity must be rejected."""
    r = client.post("/upload", data={"file": (XXE_PAYLOAD, "evil.xml")},
                    content_type="multipart/form-data")
    data = r.data.decode()
    assert r.status_code in (400, 422), (
        "XXE vulnerability: external entity was processed. "
        "Use defusedxml.ElementTree instead of lxml with default settings."
    )
    assert "root:" not in data, (
        "XXE vulnerability: /etc/passwd contents were returned in response!"
    )


def test_billion_laughs_blocked(client):
    """Billion laughs DoS payload must be rejected."""
    r = client.post("/upload", data={"file": (BILLION_LAUGHS, "dos.xml")},
                    content_type="multipart/form-data")
    assert r.status_code in (400, 422), (
        "Billion laughs attack not blocked. "
        "defusedxml blocks this automatically."
    )
