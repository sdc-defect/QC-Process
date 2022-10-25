import tensorflow as tf


# Edit
class MyModel1(tf.keras.Model):
    def __init__(self):
        super(MyModel1, self).__init__()
        self.base = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3))
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.2)
        self.outputs = tf.keras.layers.Dense(2, activation="softmax")

    def call(self, x):
        x = self.base(x)
        x = self.headModel2(x)
        x = self.headModel3(x)

        return self.outputs(x)


class MyModel2(tf.keras.Model):
    def __init__(self):
        super(MyModel2, self).__init__()
        self.base = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3))
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.5)
        self.outputs = tf.keras.layers.Dense(2, activation="softmax")

    def call(self, x):
        x = self.base(x)
        x = self.headModel2(x)
        x = self.headModel3(x)

        return self.outputs(x)
