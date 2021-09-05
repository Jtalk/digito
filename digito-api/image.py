import cv2
import numpy
from numpy import array, rint, add
from skimage.filters import threshold_otsu


def from_binary(image_bytes):
    """
    Turn raw image bytes into an image tensor (incl. to-bitmap conversion if necessary).
    :param image_bytes: A raw byte array of the image file (e.g. .png, .jpg)
    :return: A [width, height, channels] bitmap tensor of the image.
    """
    npImage = numpy.fromstring(image_bytes, numpy.uint8)
    img = cv2.imdecode(npImage, cv2.IMREAD_UNCHANGED)
    return img


def threshold_binarise(image_array, threshold=None):
    """
    Performs a threshold binarisation of the source image.
    This method preserves the shape of the original image array.
    Pixels of exactly `threshold` value get rounded down (i.e. towards black)
    If threshold=None, Otsu's method will be used to determine a suitable threshold.

    This function modifies the original array

    :param image_array: a nested-lists tensor of the image
    :param threshold: a channel value to binarise at (0..1).
    :return: the same-shape array with all values replaced with 0 or 1
    """
    if threshold is None:
        image_array = image_array.astype('float')
        threshold = threshold_otsu(image_array)
    adj = 0.5 - threshold
    image_array = add(image_array, adj)
    return rint(image_array)


def crop_background(image_array, bg_intensity=1, sim_threshold=0.1):
    """
    Crops image by the edge of its meaningful contents (i.e. the smallest box
    containing all of the non-background pixels).
    It might work unstably if the image has not been binarised.
    :param image_array: a 3-dim tensor representing the image (i.e. shape=(height, width, channels))
    :param bg_intensity: intensity of background pixels. Either a number of a channel iterable
    :param sim_threshold: a threshold of same-colour intensity. I.e. colour1 in (colour2-threshold/2, colour2+threshold/2)
            means same colour for the sake of background detection
    :return: the cropped version of the image
    """
    if isinstance(bg_intensity, int):
        channel_len = len(image_array[0][0])
        bg_intensity = [bg_intensity] * channel_len
    bg_intensity = array(bg_intensity)
    edges = _find_edges(image_array, bg_intensity, sim_threshold)
    return _cut(image_array, edges)


def convert_colour(image_array, colour, transparency_colour=None):
    """
    Convert the image to another colour space with optional transparency removal.
    :param image_array: a 3-dim tensor representing the image (i.e. shape=(height, width, channels))
    :param transparency_colour: the colour to apply to transparent parts of the image
    :param color: the target OpenCV colour option.
    """
    if image_array.shape[2] == 4 and transparency_colour is not None:
        # replace transparent parts with white for BGRA
        transp_mask = image_array[:, :, 3] == 0
        channel_count = len(image_array[0][0])
        image_array[transp_mask] = [transparency_colour] * channel_count
    return cv2.cvtColor(image_array, colour)


def resize_grayscale(image_array, dims):
    """
    Handles image resize through scikit.
    Ensures the image array is 'float' (scikit gets mad with integral arrays, treating them as 0..255 images instead).
    :param image_array: a grayscale 0..1 intensity image array
    :param dims: dimentions to resize to, e.g. (28, 28)
    :return: the resized image
    """
    image_array = image_array.astype('float')
    resized = cv2.resize(image_array, dims, interpolation=cv2.INTER_CUBIC)
    return resized.reshape((dims) + (1,))


def pad(image_array, num_pixels, padding_pixel=1):
    return numpy.pad(image_array,
                     pad_width=((num_pixels, num_pixels),
                                (num_pixels, num_pixels), (0, 0)),
                     mode='constant',
                     constant_values=padding_pixel)


class Edges:
    left: int
    right: int
    top: int
    bottom: int

    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


def _find_edges(image_array, bg_intensity, sim_threshold):
    left = _find_left_edge(image_array, bg_intensity, sim_threshold)
    inv_array = [reversed(row) for row in image_array]
    right = - 1 - _find_left_edge(inv_array, bg_intensity, sim_threshold)
    transp_array = image_array.transpose(1, 0, 2)
    top = _find_left_edge(transp_array, bg_intensity, sim_threshold)
    inv_transp_array = [reversed(row) for row in transp_array]
    bottom = - 1 - _find_left_edge(inv_transp_array,
                                   bg_intensity, sim_threshold)
    return Edges(left, right, top, bottom)


def _find_left_edge(image_array, bg_intensity, sim_threshold):
    left = len(image_array)
    for row in image_array:
        row_left = next(
            iter([i for i, v in enumerate(row) if not _tensor_similar(v, bg_intensity, threshold=sim_threshold)]), -1)
        if row_left >= 0:
            left = min(left, row_left)
    if left == len(image_array):
        left = 0
    return left


def _cut(image_array, edges):
    top = edges.top if edges.top > 0 else None
    bottom = edges.bottom + 1 if edges.bottom < -1 else None
    left = edges.left if edges.left > 0 else None
    right = edges.right + 1 if edges.right < -1 else None
    return image_array[slice(top, bottom), slice(left, right)]


def _map_nested(func, l):
    if not hasattr(l, '__len__'):
        return func(l)
    else:
        return [_map_nested(func, vals) for vals in l]


def _tensor_similar(t1, t2, threshold):
    assert t1.shape == t2.shape, 'Must have been sourced from the same image array, but got %s vs %s' % (
        t1.shape, t2.shape)
    per_value = [_similar(v1, v2, threshold) for v1, v2 in zip(t1, t2)]
    return all(per_value)


def _similar(v1, v2, threshold):
    v1_lower = v1 - threshold / 2
    v1_upper = v1 + threshold / 2
    return v1_lower < v2 < v1_upper
