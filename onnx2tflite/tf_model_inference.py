import tensorflow as tf

model = tf.saved_model.load('models/x3d_m.pb')
model.trainable = False

input_tensor = tf.random.uniform([1, 3, 16, 244,244])
out = model(**{'input': input_tensor})