import tensorflow as tf
import numpy as np
from PIL import Image

class WeedClassifier:

    def __init__(self):
        pass

    @staticmethod
    def resize_img(name, width, height):
        img = Image.open(name)
        if img.size[0] < width:
            print('Image too small to be processed without risk.')
            return None
        elif img.size[1] < height:
            print('Image too small to be processed without risk.')
            return None
        img = img.resize((width, height), Image.ANTIALIAS)  # image resize filter
        return img

    def train(self, imgs, labels):
        x = 100
        y = 100
        mode = tf.estimator.ModeKeys.TRAIN

        for i in range(len(imgs)):
            img = __class__.resize_img(imgs[i], x, y)
            if img is None:
                print('Removing image %d due to size restriction.' % i)
                return None

        # Input Layer
        input_layer = tf.reshape(imgs, [-1, x, y, 1])
        # -1 is for dynamic calculation based on batch size

        # Convolutional Layer #1
        conv1 = tf.layers.conv2d(
            inputs=input_layer,
            filters=32,
            kernel_size=[5, 5],  # dimensions of filters
            padding="same",
            activation=tf.nn.relu)

        # Pooling Layer #1
        pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

        # Convolutional Layer #2 and Pooling Layer #2
        conv2 = tf.layers.conv2d(
            inputs=pool1,
            filters=64,
            kernel_size=[5, 5],
            padding="same",
            activation=tf.nn.relu)
        pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

        # Dense Layer
        pool2_flat = tf.reshape(pool2, [-1, x/4 * y/4 * 64])
        dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
        dropout = tf.layers.dropout(
            inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

        # Logits Layer
        logits = tf.layers.dense(inputs=dropout, units=2)

        # Calculate Loss
        loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

        # Configure the Training Op (for TRAIN mode)
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())

        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

import os
weeds = os.listdir('Weed-Broadleaf_Plantain_small')
plants = os.listdir('Plant-Lettuce_small')

