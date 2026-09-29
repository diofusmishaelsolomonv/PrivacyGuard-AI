from pathlib import Path
import numpy as np

class OwnerStore:
    def __init__(self, path: Path):
        self.path = Path(path)

    def exists(self):
        return self.path.exists()

    def save(self, feature):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        np.save(self.path, feature.astype(np.float32))

    def load(self):
        return np.load(self.path).astype(np.float32)
