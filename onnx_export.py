# Some standard imports
import io
import numpy as np

from torch import nn
import torch.utils.model_zoo as model_zoo
from flash.video import VideoClassificationData, VideoClassifier
import torch
from pytorchvideo.accelerator.deployment.mobile_cpu.utils.model_conversion import (
    convert_to_deployable_form,
)


# model = VideoClassifier(backbone="x3d_m", num_classes=3, pretrained=False)
model = VideoClassifier.load_from_checkpoint("x3d_m.pt")
input_sample = torch.randn(1,3, 16, 244, 244, requires_grad=True)

model.to_onnx("x3d_m.onnx", input_sample, export_params=True)
# print(model.learning_rate)
# model.load_state_dict(torch.load("x3d_m.pt")['state_dict'])
# model.eval()

# input_blob_size = (1,3, 16, 256, 256)
# input_tensor = torch.randn(input_blob_size)
# model_efficient_x3d_xs_deploy = convert_to_deployable_form(model, input_tensor)
# # Input to the model

# x = torch.randn(1,3, 16, 224, 224, requires_grad=True)
# torch_out = model(x)

# # Export the model
# torch.onnx.export(model,               # model being run
#                   x,                         # model input (or a tuple for multiple inputs)
#                   "x3d_m.onnx",   # where to save the model (can be a file or file-like object)
#                   export_params=True,        # store the trained parameter weights inside the model file
#                   opset_version=14,          # the ONNX version to export the model to
#                   do_constant_folding=True,  # whether to execute constant folding for optimization
#                   input_names = ['input'],   # the model's input names
#                   output_names = ['output'], # the model's output names
#                   dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
#                                 'output' : {0 : 'batch_size'}})

# from torch.utils.mobile_optimizer import (
#     optimize_for_mobile,
# )
# traced_model = torch.jit.trace(model_efficient_x3d_xs_deploy, input_tensor, strict=False)

# traced_model_opt = optimize_for_mobile(traced_model)

# # Export the model

# traced_model_opt.save('traced_model_opt.pt')
