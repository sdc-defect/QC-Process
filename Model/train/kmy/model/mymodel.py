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



class MyModel3(tf.keras.Model):
    def __init__(self):
        super(MyModel3, self).__init__()
        
        self.baseModel = tf.keras.applications.efficientnet_v2.EfficientNetV2B3(include_top=False, input_shape=(300, 300, 3))
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

test = MyModel3()
test.build(input_shape=(None, 300, 300, 3))
test.summary()