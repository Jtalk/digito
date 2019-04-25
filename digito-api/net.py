import logging

import cv2
import numpy
import keras
from keras import Sequential
from keras.datasets import mnist
from keras.engine.saving import model_from_yaml
from keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Flatten, Dense, Dropout
from keras.utils import to_categorical
from numpy import array
from tqdm import tqdm

from image import threshold_binarise, crop_background, pad, resize_grayscale

_MNIST_ROWS = 28
_MNIST_COLS = 28
_PADDING = 3

_VERBOSE_IMAGE_SAVE_LIMIT = 10

log = logging.getLogger('net')


class Net():
    """
    Represents a CNN network to recognise hand-written digits.

    The training routines provided train the network on the MNIST data set.

    For trivia behind coefficients and training parameters see 'README' in the root of the project.
    """
    _model: Sequential

    def __init__(self, model_yaml_file_name=None, weights_file_name=None):
        """
        Initialise the network from the files. If file names were not provided, create an empty default network.
        The empty network must be trained before being calling `recognise`.
        :param model_yaml_file_name: a model file name. The weights won't be loaded if this file is omitted.
        :param weights_file_name: a weights file name. This parameter is only respected if the model file was also provided.
        """
        if model_yaml_file_name is None:
            log.info('No .yml file were provided, creating an untrained network')
            self._model = Net._create()
        else:
            log.info('Loading the existing network from model "%s"' % model_yaml_file_name)
            self._model = Net._load_model(model_yaml_file_name)
            if weights_file_name is not None:
                log.info('Loading the existing weights from "%s"' % weights_file_name)
                self._model.load_weights(weights_file_name)

    def save(self, model_yaml_file_name, weights_file_name):
        with open(model_yaml_file_name, 'w') as model_file:
            yaml = self._model.to_yaml()
            model_file.write(yaml)
        self._model.save_weights(weights_file_name)

    def train(self, x_train, y_train, x_test, y_test):
        """
        Train the network with the parameters provided. The training sets must be nparrays
        of grayscale images, intensity 0..255
        """
        log.info('Preprocessing a training set')
        x_train = _preprocess_images(x_train)
        log.info('Preprocessing a validation set')
        x_test = _preprocess_images(x_test)
        self._model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), batch_size=64)
        score = self._model.evaluate(x_test, y_test, verbose=0)
        return score

    def recognise(self, image_array, verbose=False):
        """
        Recognise digits presented in the array
        :param image_array: an nparray of grayscale digit images, intensity 0..255
        :return: an int representing the digit recognised.
        """
        assert image_array.shape[3] == 1, \
            'The images were expected to be grayscale, but had %d channels' % image_array.shape[3]
        log.debug('Preprocessing images before feeding them to the network')
        preprocessed = _preprocess_images(image_array, verbose=verbose)
        log.debug('Image preprocessing complete')
        results = self._model.predict(preprocessed, verbose=verbose).tolist()
        log.debug('Prediction is done, interpreting the output')
        digits = []
        for result in results:
            digit = result.index(max(result))
            digits.append(digit)
        log.info('The digits were recognised as %s, data: %s' % (digits, results))
        return digits

    @staticmethod
    def _create():
        model = Sequential()
        model.add(BatchNormalization(input_shape=(_MNIST_ROWS, _MNIST_COLS, 1)))
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

        model.compile(optimizer=keras.optimizers.SGD(),
                      loss=keras.losses.categorical_crossentropy,
                      metrics=['accuracy'])

        return model

    @staticmethod
    def _load_model(model_yaml_file_name):
        with open(model_yaml_file_name, 'r') as model_file:
            yaml = model_file.read()
            return model_from_yaml(yaml)


def train_mnist(net: Net):
    x_train, y_train, x_test, y_test = _load_mnist()
    net.train(x_train, y_train, x_test, y_test)
    return net


def _load_mnist():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    img_rows, img_cols = _MNIST_ROWS, _MNIST_COLS

    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)

    x_train = numpy.subtract(255, x_train)
    x_test = numpy.subtract(255, x_test)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    log.info('x_train shape:', x_train.shape)
    log.info('%d train samples, %d test samples', x_train.shape[0], x_test.shape[0])

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    return x_train, y_train, x_test, y_test


def _preprocess_image(image, index=None, verbose=False):
    image = numpy.divide(image, 255)

    binary = threshold_binarise(image)
    if verbose and index is not None and index < _VERBOSE_IMAGE_SAVE_LIMIT:
        _save_as('img-binary-%d.bmp' % index, binary)
    cropped = crop_background(binary)
    if verbose and index is not None and index < _VERBOSE_IMAGE_SAVE_LIMIT:
        _save_as('img-cropped-%d.bmp' % index, cropped)
    resized = resize_grayscale(cropped, (_MNIST_ROWS - _PADDING * 2, _MNIST_COLS - _PADDING * 2))
    if verbose and index is not None and index < _VERBOSE_IMAGE_SAVE_LIMIT:
        _save_as('img-resized-%d.bmp' % index, resized)
    padded = pad(resized, _PADDING, padding_pixel=1)
    if verbose and index is not None and index < _VERBOSE_IMAGE_SAVE_LIMIT:
        _save_as('img-final-%d.bmp' % index, padded)
    return padded


def _preprocess_images(images_array, verbose=False):
    return array([_preprocess_image(img, index=i, verbose=verbose) for i, img in enumerate(tqdm(images_array))])


def _save_as(name, image):
    image = numpy.multiply(image, 255)
    cv2.imwrite(name, image)
