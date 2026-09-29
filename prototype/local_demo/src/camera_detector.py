import cv2

CASCADE_NAME = "haarcascade_frontalface_default.xml"

def detect_faces(frame):
    """Return face bounding boxes using OpenCV's built-in Haar cascade."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cascade_path = getattr(cv2.data, "haarcascades", "") + CASCADE_NAME
    classifier = cv2.CascadeClassifier(cascade_path)

    # Some OpenCV builds may expose the package without legacy C++ symbols.
    # Fall back to a frame-only demo rather than crashing.
    if classifier is not None and hasattr(classifier, "detectMultiScale"):
        faces = classifier.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(70, 70)
        )
        return list(faces)

    return []