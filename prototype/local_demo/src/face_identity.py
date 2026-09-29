from pathlib import Path
import cv2
import numpy as np

COSINE_THRESHOLD = 0.363

class FaceIdentity:
    def __init__(self, model_dir: Path):
        self.model_dir = Path(model_dir)
        detector_model = str(self.model_dir / "face_detection_yunet_2023mar.onnx")
        recognizer_model = str(self.model_dir / "face_recognition_sface_2021dec.onnx")
        self.detector = cv2.FaceDetectorYN.create(detector_model, "", (320, 320), 0.9, 0.3, 5000)
        self.recognizer = cv2.FaceRecognizerSF.create(recognizer_model, "")

    def detect(self, frame):
        self.detector.setInputSize((frame.shape[1], frame.shape[0]))
        _, faces = self.detector.detect(frame)
        return [] if faces is None else faces

    def embedding(self, frame, face):
        aligned = self.recognizer.alignCrop(frame, face)
        return np.asarray(self.recognizer.feature(aligned), dtype=np.float32).reshape(1, -1)

    def similarity(self, owner_feature, query_feature):
        return float(self.recognizer.match(owner_feature, query_feature, cv2.FaceRecognizerSF_FR_COSINE))

    def is_owner(self, owner_feature, query_feature):
        score = self.similarity(owner_feature, query_feature)
        return score >= COSINE_THRESHOLD, score
