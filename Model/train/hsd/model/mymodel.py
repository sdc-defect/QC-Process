import tensorflow as tf


# Edit
class MyModel1(tf.keras.Model):
    def __init__(self):
        super(MyModel1, self).__init__()
        self.base = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False, weights="imagenet",
                                                                           input_shape=(300, 300, 3), pooling='avg')
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


class MyModel14(tf.keras.Model):
    def __init__(self):
        super(MyModel14, self).__init__()
        
        self.baseModel = tf.keras.applications.resnet50.ResNet50(include_top=False, input_shape=(300, 300, 3))
        self.norm = tf.keras.layers.BatchNormalization()
        self.activation = tf.keras.layers.ReLU()
        #  headModel1, headModeal3 Dropout을 0.3 -> 0.7 로 0.1씩 증가
        self.headModel1 = tf.keras.layers.Dropout(0.3)
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.3)
        self.outputs = tf.keras.layers.Dense(2, activation="softmax")
    
    def call(self, x):
        x = self.baseModel(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.headModel1(x)
        x = self.headModel2(x)
        x = self.headModel3(x)
        
        return self.outputs(x)

class MyModel15(tf.keras.Model):
    def __init__(self):
        super(MyModel15, self).__init__()
        
        self.baseModel = tf.keras.applications.resnet50.ResNet50(include_top=False, input_shape=(300, 300, 3))
        self.norm = tf.keras.layers.BatchNormalization()
        self.activation = tf.keras.layers.ReLU()
        #  headModel1, headModeal3 Dropout을 0.3 -> 0.7 로 0.1씩 증가
        self.headModel1 = tf.keras.layers.Dropout(0.4)
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.4)
        self.outputs = tf.keras.layers.Dense(2, activation="softmax")
    
    def call(self, x):
        x = self.baseModel(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.headModel1(x)
        x = self.headModel2(x)
        x = self.headModel3(x)
        
        return self.outputs(x)

class MyModel16(tf.keras.Model):
    def __init__(self):
        super(MyModel16, self).__init__()
        
        self.baseModel = tf.keras.applications.resnet50.ResNet50(include_top=False, input_shape=(300, 300, 3))
        self.norm = tf.keras.layers.BatchNormalization()
        self.activation = tf.keras.layers.ReLU()
        #  headModel1, headModeal3 Dropout을 0.3 -> 0.7 로 0.1씩 증가
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

test = MyModel2()
test.build(input_shape=(None, 300, 300, 3))
test.summary()