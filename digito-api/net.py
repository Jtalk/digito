import logging

import keras
import keras.losses
import numpy
from keras import Sequential
from keras.datasets import mnist
from keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Flatten, Dense, Dropout
from keras.models import load_model
from keras.optimizer_v1 import SGD
from keras.utils.np_utils import to_categorical

from config import MNIST_ROWS, MNIST_COLS, PADDING
from image import preprocess

log = logging.getLogger('net')


class Net():
    """
    Represents a CNN network to recognise hand-written digits.

    The training routines provided train the network on the MNIST data set.

    For trivia behind coefficients and training parameters see 'README' in the root of the project.
    """
    _model: Sequential

    def __init__(self, model_path=None, compile=True):
        """
        Initialise the network from the files. If file names were not provided, create an empty default network.
        The empty network must be trained before being calling `recognise`.
        :param model_path: a model path to load.
        :param compile: compile the loaded model, preparing it for training.
        """
        if model_path is None:
            log.info('No model path was provided, creating an untrained network')
            self._model = Net._create()
        else:
            log.info('Loading the existing network from model "%s"' %
                     model_path)
            self._model = Net._load_model(model_path, compile=compile)

    def save(self, model_path):
        self._model.save(model_path)
        self._model.save_weights(model_path)

    def train(self, x_train, y_train, x_test, y_test):
        """
        Train the network with the parameters provided. The training sets must be nparrays
        of grayscale images, intensity 0..255
        """
        log.info('Preprocessing the training set')
        x_train = preprocess(x_train, rows=MNIST_ROWS,
                             cols=MNIST_COLS, padding=PADDING)
        log.info('Preprocessing the validation set')
        x_test = preprocess(x_test, rows=MNIST_ROWS,
                            cols=MNIST_COLS, padding=PADDING)
        self._model.fit(x_train, y_train, epochs=10,
                        validation_data=(x_test, y_test), batch_size=64)
        score = self._model.evaluate(x_test, y_test, verbose=0)
        return score

    def recognise(self, image_array, verbose=False):
        """
        Recognise digits presented in the array
        :param image_array: an nparray of grayscale digit images, intensity 0..255
        :return: The list of predictions for further classification (see recognition.py)
        """
        return self._model.predict(image_array, verbose=verbose).tolist()


    @staticmethod
    def _create():
        model = Sequential()
        model.add(BatchNormalization(
            input_shape=(MNIST_ROWS, MNIST_COLS, 1)))
        model.add(Conv2D(filters=32, kernel_size=(4, 4)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Conv2D(filters=64, kernel_size=(9, 9)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Conv2D(filters=64, kernel_size=(9, 9)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPool2D(pool_size=(2, 2)))
        model.add(Flatten('channels_last'))
        model.add(Dense(500, activation='relu'))
        model.add(Dropout(rate=0.4))
        model.add(Dense(10, activation='softmax'))

        model.compile(optimizer=SGD(),
                      loss=keras.losses.categorical_crossentropy,
                      metrics=['accuracy'])

        return model

    @staticmethod
    def _load_model(model_path, compile=True):
        model = load_model(model_path, compile=compile)
        return model


def train_mnist(net: Net):
    x_train, y_train, x_test, y_test = _load_mnist()
    net.train(x_train, y_train, x_test, y_test)
    return net


def _load_mnist():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    img_rows, img_cols = MNIST_ROWS, MNIST_COLS

    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)

    x_train = numpy.subtract(255, x_train)
    x_test = numpy.subtract(255, x_test)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    log.info('x_train shape: %s', x_train.shape)
    log.info('%d train samples, %d test samples',
             x_train.shape[0], x_test.shape[0])

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    return x_train, y_train, x_test, y_test
