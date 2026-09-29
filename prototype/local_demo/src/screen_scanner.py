import re
from PIL import ImageGrab
import pytesseract

SENSITIVE_PATTERNS = {
    "OTP": re.compile(r"(?i)\b(?:otp|verification\s+code|one[- ]time\s+password)\b"),
    "PASSWORD": re.compile(r"(?i)\b(?:password|passcode|pin)\b"),
    "ACCOUNT": re.compile(r"(?i)\b(?:account\s+number|bank\s+account|ifsc|card\s+number)\b"),
    "IDENTITY": re.compile(r"(?i)\b(?:aadhaar|passport|pan\s+card|government\s+id|identity)\b"),
    "CONFIDENTIAL": re.compile(r"(?i)\b(?:confidential|internal\s+only|private|restricted)\b"),
}

def scan_screen():
    image = ImageGrab.grab(all_screens=True)
    text = pytesseract.image_to_string(image).strip()
    hits = [name for name, pattern in SENSITIVE_PATTERNS.items() if pattern.search(text or "")]
    highly_sensitive = any(x in hits for x in ("PASSWORD", "IDENTITY"))
    return image, text, hits, bool(hits), highly_sensitive
