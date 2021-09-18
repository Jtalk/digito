import logging
import os

import cv2

from client import TensorflowClient
from image import convert_colour, from_binary, preprocess, adjust_dimensions
from net import Net, train_mnist, MNIST_COLS, MNIST_ROWS, PADDING, classify, verify

_LOCATION = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_LOCATION, 'model')

_VERBOSE = int(os.environ['VERBOSE'] if 'VERBOSE' in os.environ else 0) > 0

log = logging.getLogger('recognition')


class Recognition:

    def __init__(self, client: TensorflowClient):
        self.client = client

    def recognise(self, img):
        img = from_binary(img)
        log.debug('Converting to a grayscale image')
        img = convert_colour(img, transparency_colour=255,
                             colour=cv2.COLOR_BGRA2GRAY)
        log.debug('Adjusting dimensions for Keras')
        img = adjust_dimensions(img)
        log.debug('Preprocessing images before feeding them to the network')
        img = preprocess(img, rows=MNIST_ROWS, cols=MNIST_COLS,
                         padding=PADDING, verbose=_VERBOSE)
        log.debug('Image preprocessing complete')
        verify(img)
        log.debug('Recognising the image')
        response = self.client.recognise(img)
        return next(iter(classify(response)))

    def check(self):
        pass


def train():
    net = Net()
    net = train_mnist(net)
    net.save(_MODEL_PATH)
