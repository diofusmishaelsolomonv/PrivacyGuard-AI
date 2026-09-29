from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).parent
MODELS = ROOT / "models"
MODELS.mkdir(exist_ok=True)

FILES = {
    "face_detection_yunet_2023mar.onnx":
        "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "face_recognition_sface_2021dec.onnx":
        "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx",
}

for name, url in FILES.items():
    target = MODELS / name
    if target.exists():
        print(f"[OK] {name}")
        continue
    print(f"[DOWNLOAD] {name}")
    urlretrieve(url, target)
    print(f"[SAVED] {target}")

print("\nModels ready.")
