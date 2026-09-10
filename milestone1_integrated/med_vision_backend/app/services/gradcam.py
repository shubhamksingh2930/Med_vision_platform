import io
import numpy as np
import torch
import torchxrayvision as xrv
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from app.services.preprocessing import load_and_preprocess

class GradCAMService:
    def __init__(self):
        self.model = xrv.models.DenseNet(weights="densenet121-res224-all")
        self.model.eval()
        target_layers = [self.model.features[-1]]
        self.cam = GradCAM(model=self.model, target_layers=target_layers)

    def generate_heatmap(self, image_path: str, target_pathology_index: int) -> bytes:
        img = load_and_preprocess(image_path)
        tensor = torch.from_numpy(img[None, ...])

        grayscale_cam = self.cam(input_tensor=tensor, targets=None)[0]

        base = img[0]
        base_norm = (base - base.min()) / (base.max() - base.min() + 1e-8)
        base_rgb = np.stack([base_norm] * 3, axis=-1).astype(np.float32)

        overlay = show_cam_on_image(base_rgb, grayscale_cam, use_rgb=True)

        buf = io.BytesIO()
        Image.fromarray(overlay).save(buf, format="PNG")
        return buf.getvalue()

gradcam_service = GradCAMService()