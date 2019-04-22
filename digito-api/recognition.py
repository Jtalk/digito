import os

import cv2

from dlnetwork import DLNetwork, train_mnist
from image import convert_colour
from image_binary import from_binary

_MODEL_YAML_NAME = 'net/model.yml'
_WEIGHTS_NAME = 'net/weights.h5'

_DLNETWORK_CACHE = None
_VERBOSE = int(os.environ['VERBOSE'] if 'VERBOSE' in os.environ else 0) > 0


def recognise(img):
    img = from_binary(img)
    img = convert_colour(img, transparency_colour=255, colour=cv2.COLOR_BGRA2GRAY)
    img = _adjust_dimensions(img)
    net = _get_network()
    return next(iter(net.recognise(img, verbose=_VERBOSE)))


def prepare():
    net = DLNetwork()
    net = train_mnist(net)
    net.save(_MODEL_YAML_NAME, _WEIGHTS_NAME)


def _get_network():
    global _DLNETWORK_CACHE
    if _DLNETWORK_CACHE is None:
        _DLNETWORK_CACHE = DLNetwork(_MODEL_YAML_NAME, _WEIGHTS_NAME)
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
