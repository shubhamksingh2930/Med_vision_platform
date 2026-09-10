import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchxrayvision as xrv

os.makedirs("app/ml_models", exist_ok=True)

class ExportableDenseNet(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.features = base_model.features
        self.classifier = base_model.classifier

    def forward(self, x):
        features = self.features(x)
        out = F.relu(features, inplace=True)
        out = F.adaptive_avg_pool2d(out, (1, 1))
        out = torch.flatten(out, 1)
        out = self.classifier(out)
        return out

base_model = xrv.models.DenseNet(weights="densenet121-res224-all")
base_model.eval()

export_model = ExportableDenseNet(base_model)
export_model.eval()

dummy_input = torch.randn(1, 1, 224, 224)
output_path = "app/ml_models/densenet121-res224-all.onnx"

torch.onnx.export(
    export_model,
    dummy_input,
    output_path,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
    opset_version=18,
    dynamo=False,
)

print(f"Successfully re-exported ONNX model to {output_path}")
print("Pathologies:", base_model.pathologies)