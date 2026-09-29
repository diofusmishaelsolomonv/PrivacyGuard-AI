import re

PATTERNS = {
    "OTP": re.compile(r"\b(?:otp|verification code|one[- ]time password)\b", re.I),
    "PASSWORD": re.compile(r"\b(?:password|passcode|pin)\b", re.I),
    "ACCOUNT": re.compile(r"\b(?:account number|bank account|ifsc|card number)\b", re.I),
    "IDENTITY": re.compile(r"\b(?:aadhaar|passport|pan card|government id|identity)\b", re.I),
    "CONFIDENTIAL": re.compile(r"\b(?:confidential|internal only|private|restricted)\b", re.I),
}

def detect(text: str):
    hits = [name for name, pattern in PATTERNS.items() if pattern.search(text or "")]
    highly_sensitive = any(x in hits for x in ("PASSWORD", "IDENTITY"))
    return hits, bool(hits), highly_sensitive
