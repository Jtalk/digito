import cv2
import numpy


def from_binary(image_bytes):
    npImage = numpy.fromstring(image_bytes, numpy.uint8)
    img = cv2.imdecode(npImage, cv2.IMREAD_UNCHANGED)
    return img
