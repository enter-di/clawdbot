"""Tests for HMAC signing and verification."""

from openclaw.security.signature import sign_payload, verify_signature


def test_sign_payload_format():
    sig = sign_payload("secret", b"body")
    assert sig.startswith("sha256=")
    assert len(sig) == 71  # "sha256=" + 64 hex chars


def test_verify_valid_signature():
    secret = "mysecret"
    body = b'{"tool": "test"}'
    sig = sign_payload(secret, body)
    assert verify_signature(secret, body, sig) is True


def test_reject_tampered_body():
    secret = "mysecret"
    sig = sign_payload(secret, b"original")
    assert verify_signature(secret, b"tampered", sig) is False


def test_reject_wrong_secret():
    body = b"payload"
    sig = sign_payload("correct_secret", body)
    assert verify_signature("wrong_secret", body, sig) is False
