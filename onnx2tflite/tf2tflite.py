import tensorflow as tf


# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model('models/x3d_m.pb')
tflite_model = converter.convert()

# Save the model
with open('models/x3d_m.tflite', 'wb') as f:
    f.write(tflite_model)