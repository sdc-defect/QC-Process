import tensorflow as tf


# Edit
class MyModel(tf.keras.Model): # ksh-case 18
    def __init__(self):
        super(MyModel, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='leaky_relu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='leaky_relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='leaky_relu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='leaky_relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='leaky_relu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='leaky_relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='leaky_relu'))
        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='leaky_relu'))
        # self.sequence.append(maxpool((2, 2)))
        #
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))

        self.sequence.append(norm())
        self.sequence.append(tf.keras.layers.LeakyReLU())
        self.sequence.append(dropout(0.5))
        # parameter 수 감소 효과
        self.sequence.append(avgpool())
        self.sequence.append(dropout(0.5))
        self.sequence.append(dense(2, activation="softmax"))

    def call(self, x, training=False, mask=None):
        for layer in self.sequence:
            x = layer(x)
        return x