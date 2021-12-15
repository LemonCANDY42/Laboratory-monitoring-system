
# Install as follows:

# git clone https://github.com/onnx/onnx-tensorflow.git && cd onnx-tensorflow
# pip install -e .

import onnx
from onnx_tf.backend import prepare

#Load the ONNX model:
onnx_model = onnx.load('models/x3d_m.onnx')
#Convert with onnx-tf:
tf_rep = prepare(onnx_model)
#Export TF model:
tf_rep.export_graph('models/x3d_m')
# very slow...