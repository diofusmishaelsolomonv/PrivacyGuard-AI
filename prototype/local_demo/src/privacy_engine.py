from dataclasses import dataclass
from enum import Enum

class Action(str, Enum):
    ALLOW = "ALLOW"
    CONTROLLED_ALLOW = "CONTROLLED ALLOW"
    WARN = "WARN"
    MASK = "MASK"
    LOCK = "LOCK"

@dataclass
class Decision:
    action: Action
    risk: str
    reason: str

def decide(face_count: int, sensitive: bool, highly_sensitive: bool, authorized: bool = True) -> Decision:
    if face_count >= 2 and sensitive:
        return Decision(Action.MASK, "HIGH",
                        "Second viewer detected while sensitive content is visible")
    if not authorized and highly_sensitive:
        return Decision(Action.LOCK, "CRITICAL",
                        "Unknown user with highly sensitive content")
    if not authorized and sensitive:
        return Decision(Action.MASK, "HIGH",
                        "Unknown user with sensitive content")
    if authorized and highly_sensitive:
        return Decision(Action.CONTROLLED_ALLOW, "MEDIUM",
                        "Authorized user with highly sensitive content")
    if authorized and sensitive:
        return Decision(Action.CONTROLLED_ALLOW, "MEDIUM",
                        "Authorized user with sensitive content")
    return Decision(Action.ALLOW, "LOW",
                    "Normal content and viewing context")
