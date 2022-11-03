import tensorflow as tf


# Edit
class MyModel3(tf.keras.Model):
    def __init__(self):
        super(MyModel3, self).__init__()
        self.base = tf.keras.applications.resnet.ResNet101(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3), pooling='avg')
        self.dense_1 = tf.keras.layers.Dense(120, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(120, activation='relu')
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.dense_1(x)
        x = self.dense_2(x)

        return self.d2(x)

class MyModel4(tf.keras.Model):
    def __init__(self):
        super(MyModel4, self).__init__()
        self.base = tf.keras.applications.resnet.ResNet152(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3), pooling='avg')
        self.dense_1 = tf.keras.layers.Dense(120, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(120, activation='relu')
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.dense_1(x)
        x = self.dense_2(x)

        return self.d2(x)

class MyModel6(tf.keras.Model):
    def __init__(self):
        super(MyModel6, self).__init__()
        self.base = tf.keras.applications.inception_resnet_v2.InceptionResNetV2(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3), pooling='avg')
        self.dense_1 = tf.keras.layers.Dense(120, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(120, activation='relu')
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.dense_1(x)
        x = self.dense_2(x)

        return self.d2(x)

class MyModel7(tf.keras.Model):
    def __init__(self):
        super(MyModel7, self).__init__()
        self.base = tf.keras.applications.inception_resnet_v2.InceptionResNetV2(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3), pooling='avg')
        self.dense_1 = tf.keras.layers.Dense(120, activation='relu')
        self.dense_2 = tf.keras.layers.Dense(120, activation='relu')
        self.d2 = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, x):
        x = self.base(x)
        x = self.dense_1(x)
        x = self.dense_2(x)

        return self.d2(x)

class MyModel8(tf.keras.Model):
    def __init__(self):
        super(MyModel8, self).__init__()
        self.base = tf.keras.applications.inception_resnet_v2.InceptionResNetV2(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3), pooling='avg')
        self.norm = tf.keras.layers.BatchNormalization()
        self.activation = tf.keras.layers.ReLU()
        self.headModel1 = tf.keras.layers.Dropout(0.5)
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.5)
        self.outputs = tf.keras.layers.Dense(2, activation="softmax")

    def call(self, x):
        x = self.base(x)
        x=self.norm(x)
        x= self.headModel3(x)
        return self.outputs(x)
class MyModel9(tf.keras.Model):
    def __init__(self):
        super(MyModel9, self).__init__()
        
        self.baseModel = tf.keras.applications.resnet50.ResNet50(include_top=False, input_shape=(300, 300, 3))
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
class MyModel13(tf.keras.Model):
    def __init__(self):
        super(MyModel13, self).__init__()
        
        self.baseModel = tf.keras.applications.resnet50.ResNet50(include_top=False, input_shape=(300, 300, 3))
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

# test = MyModel13()
# test.build(input_shape=(None, 300, 300, 3))
# test.summary()
