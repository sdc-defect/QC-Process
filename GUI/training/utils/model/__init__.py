import tensorflow as tf


# Edit
class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()

        self.baseModel = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False,
                                                                                input_shape=(300, 300, 3))
        self.norm = tf.keras.layers.BatchNormalization()
        self.activation = tf.keras.layers.ReLU()
        self.headModel1 = tf.keras.layers.Dropout(0.5)
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.5)
        self.outputs = tf.keras.layers.Dense(2, activation="softmax")

    def call(self, x):
        x = self.baseModel(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.headModel1(x)
        x = self.headModel2(x)
        x = self.headModel3(x)

        return self.outputs(x)
