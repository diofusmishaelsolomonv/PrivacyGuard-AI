# PrivacyGuard AI — Architecture Specification

## 1. System Goal

PrivacyGuard AI is designed to convert real-time identity and screen context into an adaptive privacy response.

The key abstraction is:

> **Identity + Content + Context + Risk → Action**

## 2. Input Signals

### Camera signal

Used for:
- face detection
- authorized-user verification concept
- detection of an additional viewer

### Screen signal

Used for:
- sensitive-content detection
- identifying screen regions that may require protection

## 3. Privacy Risk Engine

The engine receives normalized signals from the identity and content layers.

Example reasoning:

```text
Authorized + Normal content
        → Low risk
        → Allow

Authorized + Sensitive content
        → Medium risk
        → Controlled Allow

Unknown + Sensitive content
        → High risk
        → Mask

Unknown + Highly Sensitive content
        → Critical risk
        → Lock / Warn

Second viewer + Sensitive content
        → High risk
        → Mask
```

These are illustrative policy examples, not measured model outputs.

## 4. Protection Layer

The protection layer can expose five response levels:

1. **Allow** — no additional intervention.
2. **Warn** — notify the user that privacy risk increased.
3. **Mask** — hide a sensitive region.
4. **Blur** — reduce visual readability of a region.
5. **Lock** — block or pause access to highly sensitive content.

## 5. Event Logging

A privacy event should contain only the minimum information required for a local audit trail.

Example:

```text
10:32 — Unknown user detected
10:32 — Sensitive content detected
10:32 — Privacy Shield activated
11:05 — Authorized user verified
11:05 — OTP protection released
```

## 6. Target Snapdragon Deployment

The target architecture is a Snapdragon-powered PC using on-device AI components. Qualcomm AI Hub-compatible model concepts can be evaluated for the vision components during implementation.

Candidate model categories include:
- face detection
- face verification
- vision processing

Model selection, quantization, runtime and hardware acceleration are implementation-stage decisions and should be benchmarked on the target device rather than assumed.

## 7. Privacy Principles

- Process sensitive signals locally where practical.
- Avoid unnecessary cloud round-trips.
- Request camera permission explicitly in the demo application.
- Minimize retention of sensitive information.
- Separate detection from policy decisions.
- Keep implementation claims measurable and reproducible.
