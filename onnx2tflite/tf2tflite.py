import tensorflow as tf
import sys
sys.path.append("..") 
from src.video2array import video_to_array

def representative_data_gen():
    for input_value in tf.data.Dataset.from_tensor_slices(video_to_array("../video/New directory")).batch(1).take(200):
        yield [input_value]


# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model('../models/x3d_m')

#使用动态范围量化进行转换
#现在，我们启用默认的 optimizations 标记来量化所有固定参数（例如权重
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
# converter.target_spec.supported_types = [tf.float16,]
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
    tf.lite.OpsSet.SELECT_TF_OPS,
                                       ]# tf.lite.OpsSet.SELECT_TF_OPS,,TFLITE_BUILTINS_INT8
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8
tflite_model = converter.convert()

# Save the model
with open('../models/x3d_m_Optimize_DEFAULT_int8.tflite', 'wb') as f:
    f.write(tflite_model)