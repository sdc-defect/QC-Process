import tensorflow as tf


# Edit
class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.base = tf.keras.applications.resnet50.ResNet50(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3), pooling='avg')
        self.dense_1 = tf.keras.layers.Dense(120, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(120, activation='relu')
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.dense_1(x)
        x = self.dense_2(x)

        return self.d2(x)
