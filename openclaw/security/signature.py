"""HMAC-SHA256 signing and verification for n8n webhook requests."""

import hashlib
import hmac


def sign_payload(secret: str, body: bytes) -> str:
    """Return 'sha256=<hex_digest>' for the given body."""
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify_signature(secret: str, body: bytes, signature_header: str) -> bool:
    """Constant-time comparison of expected vs received signature."""
    expected = sign_payload(secret, body)
    return hmac.compare_digest(expected, signature_header)
