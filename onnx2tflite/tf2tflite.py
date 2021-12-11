import tensorflow as tf


# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model('models/x3d_m')

#使用动态范围量化进行转换
#现在，我们启用默认的 optimizations 标记来量化所有固定参数（例如权重
# converter.optimizations = [tf.lite.Optimize.DEFAULT]
# converter.target_spec.supported_types = [tf.float16,]
converter.target_spec.supported_ops = [tf.float16,
                                       tf.lite.OpsSet.TFLITE_BUILTINS,
                                       tf.lite.OpsSet.SELECT_TF_OPS]
tflite_model = converter.convert()

# Save the model
with open('models/x3d_m_Optimize_fp16.tflite', 'wb') as f:
    f.write(tflite_model)