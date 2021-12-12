import tensorflow as tf

def representative_data_gen():
    for input_value in tf.data.Dataset.from_tensor_slices(train_images).batch(1).take(100):
        yield [input_value]


# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model('models/x3d_m')

#使用动态范围量化进行转换
#现在，我们启用默认的 optimizations 标记来量化所有固定参数（例如权重
converter.optimizations = [tf.lite.Optimize.DEFAULT]
# converter.representative_dataset = representative_data_gen
# converter.target_spec.supported_types = [tf.float16,]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
                                       tf.lite.OpsSet.SELECT_TF_OPS]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8
tflite_model = converter.convert()

# Save the model
with open('models/x3d_m_Optimize_int8.tflite', 'wb') as f:
    f.write(tflite_model)