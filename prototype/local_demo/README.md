# PrivacyGuard AI — Local Working Demo

This folder contains the first runnable proof-of-concept of PrivacyGuard AI.

## Demonstrates

- Live webcam face detection with OpenCV
- Local sensitive-content rules
- Context-aware privacy decision engine
- Authorized/unknown demo state
- Shoulder-surfing rule using face count
- Adaptive actions: ALLOW, CONTROLLED ALLOW, MASK, LOCK
- No cloud API required

## Run

```powershell
cd prototype/local_demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

## Demo flow

1. Allow camera access.
2. Keep **Authorized user** enabled.
3. Use the default OTP text.
4. The engine should show **CONTROLLED ALLOW**.
5. Turn off **Authorized user** → sensitive OTP becomes **MASK**.
6. Try `password: secret123` → highly sensitive content becomes **LOCK** for an unknown user.
7. Put a second face in the camera view → sensitive content can trigger **MASK**.

### Honest prototype boundary

This is a local proof-of-concept, not the final Snapdragon implementation. It uses OpenCV Haar Cascade for face detection and a lightweight local rule engine for content detection. It does not yet claim biometric identity verification or Qualcomm AI Hub acceleration.
