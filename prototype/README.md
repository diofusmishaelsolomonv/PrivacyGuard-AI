# Prototype

This directory describes the controlled demonstration prototype planned for PrivacyGuard AI.

## Demonstration flows

### Flow A — Authorized user

```text
Camera permission granted
        ↓
Authorized face detected
        ↓
Normal content / sensitive content
        ↓
Allow or Controlled Allow
```

### Flow B — Unknown user

```text
Unknown face / no authorized verification
        ↓
Sensitive content detected
        ↓
Privacy risk increases
        ↓
Mask / Warn / Lock
```

### Flow C — Shoulder surfing

```text
Authorized user
        ↓
Second viewer detected
        ↓
Privacy context changes
        ↓
Sensitive region protected
```

## Implementation status

The full prototype is **under development**. This directory is intentionally documentation-first so that unimplemented components are not represented as completed software.
