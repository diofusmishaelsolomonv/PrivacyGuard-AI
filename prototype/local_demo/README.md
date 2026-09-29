# PrivacyGuard AI — Automatic Local Face Recognition Demo

This is the runnable local proof-of-concept of PrivacyGuard AI.

## What is automatic now?

On first run, the user performs a one-time **Owner Enrollment**.

After that, the camera automatically:

1. Detects every visible face.
2. Extracts a local face embedding.
3. Compares each face against the enrolled owner template.
4. Labels the context as **OWNER**, **UNKNOWN**, **OWNER + UNKNOWN**, or **NO FACE**.
5. Feeds that identity context into the privacy engine.

There is no manual **Authorized user** checkbox in the recognition flow.

### Important

A computer cannot know who its owner is without an enrollment reference. The one-time enrollment creates a local owner template; recognition after that is automatic.

## Setup

From this directory:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python download_models.py
python app.py
```

The model downloader retrieves the YuNet face detector and SFace face-recognition model from the OpenCV Model Zoo. The model files are ignored by Git and stay on the local machine.

## Owner enrollment

1. Start the application.
2. Click **ENROLL / RE-ENROLL OWNER**.
3. Look at the camera with one face visible.
4. Keep your face reasonably centered and steady while samples are collected.
5. When enrollment finishes, the status becomes **OWNER: ENROLLED • AUTO RECOGNITION ON**.

The owner template is saved locally at:

```text
data/owner_embedding.npy
```

It is intentionally ignored by Git because it is biometric data.

## Automatic scenarios

### Owner + sensitive content

```text
OWNER
  +
OTP
  ↓
CONTROLLED ALLOW
```

### Unknown person + sensitive content

```text
UNKNOWN
  +
OTP
  ↓
MASK
```

### Unknown person + highly sensitive content

```text
UNKNOWN
  +
PASSWORD / ID
  ↓
LOCK
```

### Owner + second unknown viewer

```text
OWNER + UNKNOWN
  +
SENSITIVE CONTENT
  ↓
MASK
```

## Recognition model

The prototype uses **YuNet** for face detection and **SFace** for face-feature extraction and matching. OpenCV documents a cosine similarity threshold of 0.363 for its SFace example; this project starts with that value and treats it as a demo threshold rather than a security guarantee. citeturn2search6turn2search0

## Privacy boundary

All recognition is intended to run locally in this prototype. No face image or owner template is sent to a cloud API.

This is a local proof-of-concept, not a production biometric security system. Lighting, pose, camera quality and threshold selection can affect recognition results.

The next deployment stage is to map the same identity/content/risk pipeline to Snapdragon on-device AI.
