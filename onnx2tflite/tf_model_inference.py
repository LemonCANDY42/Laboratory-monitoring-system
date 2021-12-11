import tensorflow as tf

model = tf.saved_model.load('./models/x3d_m')
model.trainable = False

input_tensor = tf.random.uniform([1, 3, 16, 244,244])
out = model(**{'input.1': input_tensor})
print(out)