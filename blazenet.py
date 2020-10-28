"""Building blocks for BlazeFace backbone network."""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def zero_channel_padding(channels_to_pad):
    """Padding the tensor channels with zero."""
    paddings = tf.constant([[0, 0], [0, 0], [0, 0], [0, channels_to_pad]])

    def forward(inputs):
        return tf.pad(inputs, paddings, "CONSTANT")

    return forward


def blaze_block(filters):
    print("Fun in++++++++++++++++++++++", filters)
    block_layers = [
        layers.DepthwiseConv2D(kernel_size=(5, 5),
                               padding='valid'),
        layers.Conv2D(filters=filters,
                      kernel_size=(1, 1))]

    def forward(inputs):
        x = inputs
        for layer in block_layers:
            x = layer(x)

        # Optional layers
        inputs = layers.MaxPool2D(pool_size=(5, 5),
                                  strides=(1, 1))(inputs)
        channels_to_pad = filters - inputs.shape.as_list()[3]

        if channels_to_pad > 0:
            inputs = zero_channel_padding(channels_to_pad)(inputs)
        elif channels_to_pad < 0:
            inputs = layers.Conv2D(filters, (1, 1))(inputs)

        # Shortcut connection.
        return layers.Add()([x, inputs])

    return forward