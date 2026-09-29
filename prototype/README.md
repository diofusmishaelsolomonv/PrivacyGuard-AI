# Prototype

PrivacyGuard AI now includes a **runnable local proof-of-concept** in [local_demo/](local_demo/).

## Runnable demo

The local demo currently implements:

- Live webcam face detection
- Local sensitive-content detection
- Authorized/unknown demo state
- Shoulder-surfing rule based on face count
- Adaptive privacy actions: **ALLOW / CONTROLLED ALLOW / MASK / LOCK**
- No cloud API dependency

### Run

```powershell
cd prototype/local_demo
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

## Demonstration flows

### Flow A — Authorized user

```text
Camera
  ↓
Face detected
  ↓
Sensitive content detected
  ↓
CONTROLLED ALLOW
```

### Flow B — Unknown user

```text
Camera
  ↓
Authorized toggle OFF
  ↓
Sensitive content
  ↓
MASK / LOCK
```

### Flow C — Shoulder surfing

```text
Authorized user
  ↓
Second face detected
  ↓
Privacy risk increases
  ↓
Sensitive content → MASK
```

## Prototype boundary

This is the first local proof-of-concept, not the final Snapdragon implementation. It uses OpenCV Haar Cascade for face detection and a lightweight local rule engine for content detection.

It does **not** yet claim biometric identity verification, Qualcomm AI Hub acceleration, or production deployment. Those are planned next stages.
