import numpy as np
import skimage.io
import torchxrayvision as xrv
import torchvision

_transform = torchvision.transforms.Compose([
    xrv.datasets.XRayCenterCrop(),
    xrv.datasets.XRayResizer(224),
])

def load_and_preprocess(image_path: str) -> np.ndarray:
    img = skimage.io.imread(image_path)
    img = xrv.datasets.normalize(img, 255)

    if img.ndim == 3:
        img = img.mean(2)
    img = img[None, ...]

    img = _transform(img)
    return img.astype(np.float32)