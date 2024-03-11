# this script performs matrix multiplication using TensorFlow

import tensorflow as tf

# disable eager execution to ensure compatibility with TensorFlow 1.x
tf.compat.v1.disable_eager_execution()

# Specify the device to use for computation (in this case, GPU 0)
with tf.device('/gpu:0'):
    # Define two constant tensors 'a' and 'b'
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    
    # Perform matrix multiplication between tensors 'a' and 'b'
    c = tf.matmul(a, b)

# create a TensorFlow session to execute the computation graph
with tf.compat.v1.Session() as sess:
    # Run teh session to compute the result of matrix multiplication
    print (sess.run(c))
