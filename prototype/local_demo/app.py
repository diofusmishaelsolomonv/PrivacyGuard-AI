import sys
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE / "src"))

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from screen_scanner import scan_screen
import numpy as np

from privacy_engine import decide
from sensitive_detector import detect
from face_identity import FaceIdentity
from owner_store import OwnerStore

class PrivacyGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PrivacyGuard AI — Local Prototype")
        self.root.geometry("1160x760")
        self.root.configure(bg="#070B14")

        self.cap = cv2.VideoCapture(0)
        self.owner_store = OwnerStore(BASE / "data" / "owner_embedding.npy")
        self.identity = None
        self.owner_feature = None
        self.enrolling = False
        self.enroll_samples = []
        self.enroll_target = 12

        self.status = tk.StringVar(value="Starting camera…")
        self.identity_status = tk.StringVar(value="OWNER: NOT ENROLLED")
        self.decision = tk.StringVar(value="—")
        self.risk = tk.StringVar(value="—")
        self.reason = tk.StringVar(value="—")
        self.score = tk.StringVar(value="—")
        self.demo_text = tk.StringVar(value="OTP verification code: 482913")
        self.protected_text = tk.StringVar(value="OTP verification code: 482913")
        self.screen_status = tk.StringVar(value="Screen scan: not run")

        try:
            self.identity = FaceIdentity(BASE / "models")
            if self.owner_store.exists():
                self.owner_feature = self.owner_store.load()
                self.identity_status.set("OWNER: ENROLLED • AUTO RECOGNITION ON")
            else:
                self.identity_status.set("OWNER: NOT ENROLLED • ENROLL FIRST")
        except Exception as exc:
            self.status.set(f"AI models not ready: {exc}")

        self.build_ui()
        self.update_frame()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#0E1928", height=82)
        header.pack(fill="x")
        tk.Label(header, text="PrivacyGuard AI", fg="#F4F7FB", bg="#0E1928",
                 font=("Segoe UI", 25, "bold")).pack(side="left", padx=24, pady=16)
        tk.Label(header, text="Automatic Owner / Unknown Face Recognition • Local Prototype",
                 fg="#55D6FF", bg="#0E1928", font=("Segoe UI", 11)).pack(side="left")

        main = tk.Frame(self.root, bg="#070B14")
        main.pack(fill="both", expand=True, padx=18, pady=16)

        left = tk.Frame(main, bg="#0E1928", highlightbackground="#263A52", highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(main, bg="#0E1928", width=420, highlightbackground="#263A52", highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.video_label = tk.Label(left, bg="#05080E")
        self.video_label.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(left, textvariable=self.status, fg="#A9B8C9", bg="#0E1928",
                 font=("Segoe UI", 10)).pack(pady=(0, 6))
        tk.Label(left, textvariable=self.identity_status, fg="#55D6FF", bg="#0E1928",
                 font=("Segoe UI", 10, "bold")).pack(pady=(0, 12))

        tk.Label(right, text="PRIVACY DECISION", fg="#FF3347", bg="#0E1928",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(20, 8))
        tk.Label(right, textvariable=self.decision, fg="#F4F7FB", bg="#16273A",
                 font=("Segoe UI", 21, "bold"), padx=12, pady=12).pack(fill="x", padx=20)

        for label, var in [("Identity score", self.score), ("Risk", self.risk), ("Reason", self.reason)]:
            tk.Label(right, text=label, fg="#55D6FF", bg="#0E1928",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(12, 2))
            tk.Label(right, textvariable=var, fg="#F4F7FB", bg="#0E1928",
                     font=("Segoe UI", 9), wraplength=365, justify="left").pack(anchor="w", padx=20)

        ttk.Separator(right).pack(fill="x", padx=20, pady=14)

        tk.Label(right, text="OWNER SETUP", fg="#FF3347", bg="#0E1928",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(0, 8))
        tk.Button(right, text="ENROLL / RE-ENROLL OWNER", command=self.start_enrollment,
                  bg="#FF3347", fg="white", activebackground="#D92537",
                  activeforeground="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), padx=10, pady=8).pack(fill="x", padx=20)

        tk.Label(right,
                 text="First run: click Enroll and look at the camera. "
                      "After enrollment, recognition is automatic — no manual Authorized checkbox.",
                 fg="#A9B8C9", bg="#0E1928", font=("Segoe UI", 8),
                 wraplength=365, justify="left").pack(anchor="w", padx=20, pady=(7, 8))

        tk.Label(right, text="PROTECTED SCREEN PREVIEW", fg="#55D6FF", bg="#0E1928",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(8, 4))
        entry = tk.Entry(right, textvariable=self.demo_text, bg="#16273A",
                         fg="#F4F7FB", insertbackground="#F4F7FB", relief="flat",
                         font=("Segoe UI", 10))
        entry.pack(fill="x", padx=20, ipady=8)
        tk.Label(right, textvariable=self.protected_text, bg="#16273A",
                 fg="#F4F7FB", font=("Segoe UI", 11, "bold"),
                 anchor="w", padx=10, pady=8, wraplength=365,
                 justify="left").pack(fill="x", padx=20, pady=(6, 0))
        tk.Label(right, text="Enter sample data above. Unknown/second face → sensitive text is masked.",
                 fg="#718096", bg="#0E1928", font=("Segoe UI", 8),
                 wraplength=365, justify="left").pack(anchor="w", padx=20, pady=(4, 8))

        tk.Button(right, text="SCAN CURRENT SCREEN (OCR)", command=self.scan_current_screen,
                  bg="#1677FF", fg="white", activebackground="#125FCF",
                  activeforeground="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), padx=10, pady=8).pack(fill="x", padx=20, pady=(2, 6))
        tk.Label(right, textvariable=self.screen_status, fg="#A9B8C9", bg="#0E1928",
                 font=("Segoe UI", 8), wraplength=365, justify="left").pack(anchor="w", padx=20, pady=(0, 8))

        tk.Label(right, text="DECISION PIPELINE", fg="#FF3347", bg="#0E1928",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(8, 6))
        tk.Label(right, text="WHO → WHAT → CONTEXT → RISK → ACTION",
                 fg="#F4F7FB", bg="#0E1928", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20)
        tk.Label(right,
                 text="Owner recognition uses a local face embedding. "
                      "No face image is uploaded to a cloud service.",
                 fg="#A9B8C9", bg="#0E1928", font=("Segoe UI", 8),
                 wraplength=365, justify="left").pack(anchor="w", padx=20, pady=(8, 0))

    def scan_current_screen(self):
        try:
            image, text, hits, sensitive, highly = scan_screen()
            if not text:
                self.screen_status.set("Screen scan: no readable text detected")
                return
            self.demo_text.set(text[:300])
            self.screen_status.set(
                f"Screen OCR: {len(text)} chars • Sensitive: {', '.join(hits) if hits else 'none'}"
            )
            if hits:
                self.protected_text.set("••••••••••••  [SENSITIVE CONTENT DETECTED]")
            else:
                self.protected_text.set(text[:300])
        except Exception as exc:
            self.screen_status.set(f"Screen OCR error: {exc}")

    def start_enrollment(self):
        if self.identity is None:
            messagebox.showerror("Models not ready", "Run download_models.py first.")
            return
        self.enrolling = True
        self.enroll_samples = []
        self.identity_status.set("OWNER: ENROLLING 0/12 • LOOK AT CAMERA")
        self.status.set("Enrollment started • keep one face centered and steady")

    def finish_enrollment(self):
        if not self.enroll_samples:
            self.enrolling = False
            self.identity_status.set("OWNER: NOT ENROLLED")
            return
        feature = np.mean(np.vstack(self.enroll_samples), axis=0, keepdims=True).astype(np.float32)
        norm = np.linalg.norm(feature)
        if norm > 0:
            feature /= norm
        self.owner_store.save(feature)
        self.owner_feature = feature
        self.enrolling = False
        self.identity_status.set("OWNER: ENROLLED • AUTO RECOGNITION ON")
        self.status.set("Owner enrollment complete • recognition is now automatic")

    def update_frame(self):
        ok, frame = self.cap.read()
        if not ok:
            self.status.set("Camera unavailable — check camera permission")
            self.root.after(300, self.update_frame)
            return

        owner_present = False
        unknown_present = False
        best_score = None
        try:
            faces = self.identity.detect(frame) if self.identity else []
        except Exception as exc:
            faces = []
            self.status.set(f"Face AI error: {exc}")

        if self.enrolling:
            if len(faces) == 1:
                try:
                    feature = self.identity.embedding(frame, faces[0])
                    self.enroll_samples.append(feature)
                    self.identity_status.set(
                        f"OWNER: ENROLLING {len(self.enroll_samples)}/{self.enroll_target} • KEEP STEADY"
                    )
                    self.status.set(
                        f"Collecting owner face samples • {len(self.enroll_samples)}/{self.enroll_target}"
                    )
                    if len(self.enroll_samples) >= self.enroll_target:
                        self.finish_enrollment()
                except Exception as exc:
                    self.status.set(f"Enrollment sample error: {exc}")

        if not self.enrolling and self.owner_feature is not None and self.identity:
            for face in faces:
                try:
                    feature = self.identity.embedding(frame, face)
                    is_owner, score = self.identity.is_owner(self.owner_feature, feature)
                    best_score = score if best_score is None else max(best_score, score)
                    if is_owner:
                        owner_present = True
                    else:
                        unknown_present = True
                except Exception:
                    unknown_present = True

        if len(faces) == 0:
            identity_label = "NO FACE"
        elif self.owner_feature is None:
            identity_label = "ENROLL OWNER"
        elif owner_present and unknown_present:
            identity_label = "OWNER + UNKNOWN"
        elif owner_present:
            identity_label = "OWNER"
        else:
            identity_label = "UNKNOWN"

        for face in faces:
            x, y, w, h = [int(v) for v in face[:4]]
            color = (70, 220, 110) if self.owner_feature is not None and owner_present else (0, 170, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        hits, sensitive, highly = detect(self.demo_text.get())

        if self.owner_feature is None:
            # No owner is trusted until the user completes enrollment.
            d = decide(len(faces), sensitive, highly, authorized=False)
        else:
            if owner_present:
                # If a second unknown face is present, treat it as a shoulder-surfing context.
                if unknown_present or len(faces) >= 2:
                    d = decide(2, sensitive, highly, authorized=True)
                else:
                    d = decide(1, sensitive, highly, authorized=True)
            else:
                d = decide(len(faces), sensitive, highly, authorized=False)

        self.decision.set(d.action.value)
        self.risk.set(d.risk)
        if d.action.value in ("MASK", "LOCK"):
            self.protected_text.set("••••••••••••  [SENSITIVE CONTENT MASKED]")
        else:
            self.protected_text.set(self.demo_text.get())
        self.reason.set(
            f"{identity_label} • {d.reason}"
            + (f" • cosine={best_score:.3f}" if best_score is not None else "")
        )
        self.score.set(f"{best_score:.3f}" if best_score is not None else "—")
        self.status.set(
            f"Camera active • {len(faces)} face(s) • {identity_label} • "
            f"Sensitive: {', '.join(hits) if hits else 'none'}"
        )

        if d.action.value in ("MASK", "LOCK"):
            overlay = frame.copy()
            cv2.rectangle(overlay, (20, 20), (frame.shape[1]-20, 105), (7, 11, 20), -1)
            frame = cv2.addWeighted(overlay, 0.88, frame, 0.12, 0)
            cv2.putText(frame, d.action.value, (45, 75),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.25, (51, 51, 255), 3)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(rgb)
        im.thumbnail((680, 570))
        photo = ImageTk.PhotoImage(im)
        self.video_label.configure(image=photo)
        self.video_label.image = photo
        self.root.after(80, self.update_frame)

    def close(self):
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

root = tk.Tk()
app = PrivacyGuardApp(root)
root.protocol("WM_DELETE_WINDOW", app.close)
root.mainloop()
