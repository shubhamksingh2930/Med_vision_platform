import onnxruntime as ort
import torchxrayvision as xrv
from app.services.preprocessing import load_and_preprocess

# Load metadata for pathology names
_PATHOLOGIES = xrv.models.DenseNet(weights="densenet121-res224-all").pathologies

class InferenceService:
    def __init__(self, onnx_path: str = "app/ml_models/densenet121-res224-all.onnx"):
        self.session = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name

    def run(self, image_path: str) -> dict:
        img = load_and_preprocess(image_path)
        batch = img[None, ...]  # shape: (1, 1, 224, 224)

        outputs = self.session.run(None, {self.input_name: batch})
        probs = outputs[0][0]  # shape: (18,)

        return {p: float(v) for p, v in zip(_PATHOLOGIES, probs)}

inference_service = InferenceService()