import logging
import os

import cv2

from image import convert_colour, from_binary
from net import Net, train_mnist

_LOCATION = os.path.dirname(os.path.abspath(__file__))

_MODEL_YAML_NAME = os.path.join(_LOCATION, 'model', 'model.yml')
_WEIGHTS_NAME = os.path.join(_LOCATION, 'model', 'weights.h5')

_DLNETWORK_CACHE = None
_VERBOSE = int(os.environ['VERBOSE'] if 'VERBOSE' in os.environ else 0) > 0

log = logging.getLogger('recognition')


def recognise(img):
    img = from_binary(img)
    log.debug('Converting to a grayscale image')
    img = convert_colour(img, transparency_colour=255, colour=cv2.COLOR_BGRA2GRAY)
    log.debug('Adjusting dimensions for Keras')
    img = _adjust_dimensions(img)
    net = _get_network()
    log.debug('Recognising the image')
    return next(iter(net.recognise(img, verbose=_VERBOSE)))


def check():
    _get_network()


def preload():
    global _DLNETWORK_CACHE
    log.info('Loading the network')
    _DLNETWORK_CACHE = Net(_MODEL_YAML_NAME, _WEIGHTS_NAME)
    log.info('The network was successfully loaded')


def train():
    net = Net()
    net = train_mnist(net)
    net.save(_MODEL_YAML_NAME, _WEIGHTS_NAME)


def _get_network():
    global _DLNETWORK_CACHE
    log.debug('Getting a network instance')
    if _DLNETWORK_CACHE is None:
        preload()
    return _DLNETWORK_CACHE


def _adjust_dimensions(image_array):
    """
    Converts the image array to a standard representation for the network
    :param image_array:
    :return:
    """
    shape_len = len(image_array.shape)
    if shape_len == 2:
        return image_array.reshape((1, image_array.shape[0], image_array.shape[1], 1))
    elif shape_len == 3:
        return image_array.reshape(((1, image_array.shape[0], image_array.shape[1], image_array.shape[2])))
    else:
        raise ValueError('Unsupported image tensor shape %s' % image_array.shape)
