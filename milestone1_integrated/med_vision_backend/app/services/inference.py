class InferenceService:
    def run(self, file_url: str) -> dict:
        """
        Stub for M3. Will run ONNX preprocessing + inference + GradCAM.
        Returns a dict shape that persistence.py expects.
        """
        return {
            "prediction_result": '{"pneumonia_probability": 0.0, "note": "stub result"}',
            "heatmap_image_url": None,
        }

inference_service = InferenceService()