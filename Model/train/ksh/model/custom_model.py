import tensorflow as tf

# Edit
class MyCustomModel(tf.keras.Model): # ksh-case 16
    def __init__(self):
        super(MyCustomModel, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu'))
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(maxpool((2, 2)))
        #
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))

        self.sequence.append(norm())
        self.sequence.append(tf.keras.layers.ReLU())
        self.sequence.append(dropout(0.5))
        # parameter 수 감소 효과
        self.sequence.append(avgpool())
        self.sequence.append(dropout(0.5))
        self.sequence.append(dense(2, activation="softmax"))

    def call(self, x, training=False, mask=None):
        for layer in self.sequence:
            x = layer(x)
        return x



class MyCustomModel2(tf.keras.Model): # hsd-case 18
    def __init__(self):
        super(MyCustomModel2, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(maxpool((2, 2)))
        #
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))

        self.sequence.append(norm())
        self.sequence.append(tf.keras.layers.ReLU())
        self.sequence.append(dropout(0.5))
        # parameter 수 감소 효과
        self.sequence.append(avgpool())
        self.sequence.append(dropout(0.5))
        self.sequence.append(dense(2, activation="softmax"))

    def call(self, x, training=False, mask=None):
        for layer in self.sequence:
            x = layer(x)
        return x



class MyCustomModel3(tf.keras.Model): # ksh-case 17
    def __init__(self):
        super(MyCustomModel3, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(norm())
        # self.sequence.append(maxpool((2, 2)))
        #
        # self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(maxpool((2, 2)))
        #
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))

        self.sequence.append(norm())
        self.sequence.append(tf.keras.layers.ReLU())
        self.sequence.append(dropout(0.5))
        # parameter 수 감소 효과
        self.sequence.append(avgpool())
        self.sequence.append(dropout(0.5))
        self.sequence.append(dense(2, activation="softmax"))

    def call(self, x, training=False, mask=None):
        for layer in self.sequence:
            x = layer(x)
        return x


class MyCustomModel4(tf.keras.Model): # hsd-case 19
    def __init__(self):
        super(MyCustomModel4, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='elu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='elu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='elu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='elu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='elu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='elu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='elu'))
        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='elu'))
        # self.sequence.append(maxpool((2, 2)))
        #
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(conv2d(512, (3, 3), padding='same', activation='relu'))

        self.sequence.append(norm())
        self.sequence.append(tf.keras.layers.ELU())
        self.sequence.append(dropout(0.5))
        # parameter 수 감소 효과
        self.sequence.append(avgpool())
        self.sequence.append(dropout(0.5))
        self.sequence.append(dense(2, activation="softmax"))

    def call(self, x, training=False, mask=None):
        for layer in self.sequence:
            x = layer(x)
        return x


class MyCustomModel5(tf.keras.Model): # ksh-case 18
    def __init__(self):
        super(MyCustomModel5, self).__init__()

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



class MyCustomModel6(tf.keras.Model): # ksh-case 19
    def __init__(self):
        super(MyCustomModel6, self).__init__()

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



class MyCustomModel7(tf.keras.Model): # ksh-case 20
    def __init__(self):
        super(MyCustomModel7, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        # self.sequence.append(norm())
        # self.sequence.append(maxpool((2, 2)))

        # self.sequence.append(conv2d(256, (3, 3), padding='same', activation='leaky_relu'))
        # self.sequence.append(conv2d(256, (3, 3), padding='same', activation='leaky_relu'))
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



class MyCustomModel8(tf.keras.Model): # ksh-case 21
    def __init__(self):
        super(MyCustomModel8, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
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



class MyCustomModel9(tf.keras.Model): # ksh-case 22
    def __init__(self):
        super(MyCustomModel9, self).__init__()

        conv2d = tf.keras.layers.Conv2D
        maxpool = tf.keras.layers.MaxPool2D
        avgpool = tf.keras.layers.GlobalAveragePooling2D
        norm = tf.keras.layers.BatchNormalization
        dense = tf.keras.layers.Dense
        dropout = tf.keras.layers.Dropout

        self.sequence = list()

        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu', input_shape=(300, 300, 3)))
        self.sequence.append(conv2d(32, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(dropout(0.5))
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(64, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(dropout(0.5))
        self.sequence.append(maxpool((2, 2)))


        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(128, (3, 3), padding='same', activation='relu'))
        self.sequence.append(norm())
        self.sequence.append(dropout(0.5))
        self.sequence.append(maxpool((2, 2)))

        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))
        self.sequence.append(conv2d(256, (3, 3), padding='same', activation='relu'))


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

test = MyCustomModel9()
test.build(input_shape=(None, 300, 300, 3))
test.summary()