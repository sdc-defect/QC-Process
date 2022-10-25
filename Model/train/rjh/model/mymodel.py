import tensorflow as tf


# Edit
class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.base = tf.keras.applications.efficientnet.EfficientNetB3(include_top=False, weights="imagenet",
                                                                      input_shape=(300, 300, 3), pooling='max')
        self.dense_1 = tf.keras.layers.Dense(120, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(120, activation='relu')
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.dense_1(x)
        x = self.dense_2(x)

        return self.d2(x)


class MyModel2(tf.keras.Model):
    def __init__(self):
        super(MyModel2, self).__init__()
        self.base = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False,
                                                                           input_shape=(300, 300, 3))
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.2)
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.headModel2(x)
        x = self.headModel3(x)

        return self.d2(x)
