import tensorflow as tf


class EB0(tf.keras.Model):
    def __init__(self):
        super(EB0, self).__init__()
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


class EB1(tf.keras.Model):
    def __init__(self):
        super(EB1, self).__init__()
        self.base = tf.keras.applications.efficientnet_v2.EfficientNetV2B1(include_top=False,
                                                                           input_shape=(300, 300, 3))
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.2)
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.headModel2(x)
        x = self.headModel3(x)

        return self.d2(x)


class EB2(tf.keras.Model):
    def __init__(self):
        super(EB2, self).__init__()
        self.base = tf.keras.applications.efficientnet_v2.EfficientNetV2B2(include_top=False,
                                                                           input_shape=(300, 300, 3))
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.2)
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.headModel2(x)
        x = self.headModel3(x)

        return self.d2(x)
