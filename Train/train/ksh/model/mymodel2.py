import tensorflow as tf


# Edit
class EfficientNetB4(tf.keras.Model):
    def __init__(self):
        super(EfficientNetB4, self).__init__()
        
        self.baseModel = tf.keras.applications.efficientnet.EfficientNetB4(weights="imagenet", include_top=False, 
                                                                    input_shape=(380, 380, 3))
        self.headModel2 = tf.keras.layers.GlobalAveragePooling2D()
        self.headModel3 = tf.keras.layers.Dropout(0.2)
        self.outputs = tf.keras.layers.Dense(2, activation="softmax")
    
    def call(self, x):
        x = self.baseModel(x)
        x = self.headModel2(x)
        x = self.headModel3(x)

        return self.outputs(x)
