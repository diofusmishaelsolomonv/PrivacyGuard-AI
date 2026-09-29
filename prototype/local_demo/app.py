import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))
from privacy_engine import decide
from sensitive_detector import detect
from camera_detector import detect_faces

class PrivacyGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PrivacyGuard AI — Local Prototype")
        self.root.geometry("1120x720")
        self.root.configure(bg="#070B14")
        self.cap = cv2.VideoCapture(0)
        self.authorized = tk.BooleanVar(value=True)
        self.demo_text = tk.StringVar(value="OTP verification code: 482913")
        self.status = tk.StringVar(value="Starting camera…")
        self.decision = tk.StringVar(value="—")
        self.risk = tk.StringVar(value="—")
        self.reason = tk.StringVar(value="—")
        self.face_count = 0
        self.build_ui()
        self.update_frame()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#0E1928", height=74)
        header.pack(fill="x")
        tk.Label(header, text="PrivacyGuard AI", fg="#F4F7FB", bg="#0E1928",
                 font=("Segoe UI", 24, "bold")).pack(side="left", padx=24, pady=16)
        tk.Label(header, text="Adaptive On-Device Privacy Firewall • Local Prototype",
                 fg="#55D6FF", bg="#0E1928", font=("Segoe UI", 11)).pack(side="left")

        main = tk.Frame(self.root, bg="#070B14")
        main.pack(fill="both", expand=True, padx=18, pady=16)
        left = tk.Frame(main, bg="#0E1928", highlightbackground="#263A52", highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = tk.Frame(main, bg="#0E1928", width=410, highlightbackground="#263A52", highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.video_label = tk.Label(left, bg="#05080E")
        self.video_label.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(left, textvariable=self.status, fg="#A9B8C9", bg="#0E1928",
                 font=("Segoe UI", 10)).pack(pady=(0, 10))

        tk.Label(right, text="PRIVACY DECISION", fg="#FF3347", bg="#0E1928",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(20, 8))
        tk.Label(right, textvariable=self.decision, fg="#F4F7FB", bg="#16273A",
                 font=("Segoe UI", 22, "bold"), padx=12, pady=12).pack(fill="x", padx=20)

        for label, var in [("Risk", self.risk), ("Reason", self.reason)]:
            tk.Label(right, text=label, fg="#55D6FF", bg="#0E1928",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(14, 2))
            tk.Label(right, textvariable=var, fg="#F4F7FB", bg="#0E1928",
                     font=("Segoe UI", 10), wraplength=360, justify="left").pack(anchor="w", padx=20)

        ttk.Separator(right).pack(fill="x", padx=20, pady=16)
        tk.Label(right, text="DEMO CONTROLS", fg="#FF3347", bg="#0E1928",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(0, 8))
        tk.Checkbutton(right, text="Authorized user", variable=self.authorized,
                        fg="#F4F7FB", bg="#0E1928", activebackground="#0E1928",
                        activeforeground="#F4F7FB", selectcolor="#16273A",
                        font=("Segoe UI", 10)).pack(anchor="w", padx=20)

        tk.Label(right, text="Demo screen content", fg="#55D6FF", bg="#0E1928",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(12, 4))
        entry = tk.Entry(right, textvariable=self.demo_text, bg="#16273A",
                         fg="#F4F7FB", insertbackground="#F4F7FB", relief="flat",
                         font=("Segoe UI", 10))
        entry.pack(fill="x", padx=20, ipady=8)
        tk.Label(right, text="Try: OTP / password / Aadhaar / confidential",
                 fg="#718096", bg="#0E1928", font=("Segoe UI", 8)).pack(anchor="w", padx=20, pady=(4, 10))

        tk.Label(right, text="HOW IT WORKS", fg="#FF3347", bg="#0E1928",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(12, 8))
        tk.Label(right, text="WHO → WHAT → RISK → ACTION", fg="#F4F7FB",
                 bg="#0E1928", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20)
        tk.Label(right,
                 text="The local demo uses face count for the shoulder-surfing scenario. "
                      "The prototype does not claim biometric identity verification yet.",
                 fg="#A9B8C9", bg="#0E1928", font=("Segoe UI", 8),
                 wraplength=360, justify="left").pack(anchor="w", padx=20, pady=(8, 0))

    def update_frame(self):
        ok, frame = self.cap.read()
        if not ok:
            self.status.set("Camera unavailable — check camera permission")
            self.root.after(300, self.update_frame)
            return

        try:
            faces = detect_faces(frame)
        except Exception as exc:
            self.status.set(f"Face detector error: {exc}")
            faces = []

        self.face_count = len(faces)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (85, 214, 255), 2)

        hits, sensitive, highly = detect(self.demo_text.get())
        d = decide(self.face_count, sensitive, highly, self.authorized.get())
        self.decision.set(d.action.value)
        self.risk.set(d.risk)
        self.reason.set(d.reason)
        self.status.set(
            f"Camera active • {self.face_count} face(s) detected • "
            f"Sensitive signals: {', '.join(hits) if hits else 'none'}"
        )

        if d.action.value in ("MASK", "LOCK"):
            overlay = frame.copy()
            cv2.rectangle(overlay, (20, 20), (frame.shape[1]-20, 95), (7, 11, 20), -1)
            frame = cv2.addWeighted(overlay, 0.88, frame, 0.12, 0)
            cv2.putText(frame, d.action.value, (45, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.35, (51, 51, 255), 3)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(rgb)
        im.thumbnail((650, 560))
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
