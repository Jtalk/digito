from unittest import TestCase

import cv2
from numpy import array

import image
from image_binary import from_binary


class ImageTest_threshold_binarise(TestCase):

    def test_plain(self):
        vals = array([0.1, 0, 0.4, 0.6, 0.8, 1])
        result = image.threshold_binarise(vals, threshold=0.5)
        self.assertEqual([0, 0, 0, 1, 1, 1], result.tolist())

    def test_threshold_down(self):
        vals = array([0.5])
        result = image.threshold_binarise(vals, threshold=0.5)
        self.assertEqual([0], result.tolist())

    def test_custom_threshold(self):
        vals = array([0.01, 0.03])
        result = image.threshold_binarise(vals, threshold=0.02)
        self.assertEqual([0, 1], result.tolist())

    def test_preserves_shape(self):
        vals = array([
            [
                [0.1, 0.2, 0.3],
                [0.8, 0.1, 0.3],
            ],
            [
                [0.4, 0.7, 0.81],
                [0.3, 0.1, 0.18],
            ],
        ])
        result = image.threshold_binarise(vals, threshold=0.5)
        self.assertEqual([
            [
                [0, 0, 0],
                [1, 0, 0]
            ],
            [
                [0, 1, 1],
                [0, 0, 0],
            ],
        ], result.tolist())

    def test_auto_threshold(self):
        vals = array([
            [
                [1],
                [1],
                [1],
                [1],
                [1],
            ],
            [
                [1],
                [1],
                [0.9],
                [1],
                [1],
            ],
            [
                [1],
                [0.9],
                [0.9],
                [0.9],
                [1],
            ],
        ])
        result = image.threshold_binarise(vals)
        expected = array([
            [
                [1],
                [1],
                [1],
                [1],
                [1],
            ],
            [
                [1],
                [1],
                [0],
                [1],
                [1],
            ],
            [
                [1],
                [0],
                [0],
                [0],
                [1],
            ],
        ])
        self.assertEqual(expected.tolist(), result.tolist())


class ImageTest_crop_background(TestCase):
    def test_plain(self):
        img = array([
            [
                [1],
                [1],
                [1],
                [1],
                [1],
            ],
            [
                [1],
                [1],
                [0],
                [1],
                [1],
            ],
            [
                [1],
                [0],
                [0],
                [0],
                [1],
            ],
            [
                [1],
                [1],
                [1],
                [1],
                [1],
            ],
            [
                [1],
                [1],
                [1],
                [1],
                [1],
            ],
        ])
        result = image.crop_background(img, bg_intensity=1)
        expected = array([
            [
                [1],
                [0],
                [1],
            ],
            [
                [0],
                [0],
                [0],
            ],
        ])
        self.assertEqual(expected.tolist(), result.tolist())

    def test_no_cut(self):
        img = array([
            [
                [1],
                [0],
                [1],
                [1],
                [1],
            ],
            [
                [1],
                [1],
                [0],
                [1],
                [1],
            ],
            [
                [1],
                [0],
                [0],
                [0],
                [1],
            ],
            [
                [0],
                [1],
                [1],
                [1],
                [0],
            ],
            [
                [1],
                [1],
                [0],
                [1],
                [1],
            ],
        ])
        result = image.crop_background(img, bg_intensity=1)
        self.assertEqual(img.tolist(), result.tolist())

    def test_no_background(self):
        img = array([
            [
                [0],
                [0],
                [0],
                [0],
                [0],
            ],
            [
                [0],
                [0],
                [0],
                [0],
                [0],
            ],
            [
                [0],
                [0],
                [0],
                [0],
                [0],
            ],
            [
                [0],
                [0],
                [0],
                [0],
                [0],
            ],
            [
                [0],
                [0],
                [0],
                [0],
                [0],
            ],
        ])
        result = image.crop_background(img, bg_intensity=1)
        self.assertEqual(img.tolist(), result.tolist())

    def test_multichannel(self):
        img = array([
            [
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
            ],
            [
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [0.01, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
            ],
            [
                [1, 0.5, 0.3],
                [0, 0.5, 0.31],
                [0, 0.51, 0.31],
                [0, 0.5, 0.29],
                [1, 0.5, 0.3],
            ],
            [
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
            ],
            [
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
                [1, 0.5, 0.3],
            ],
        ])
        result = image.crop_background(img, bg_intensity=[1, 0.5, 0.3])
        expected = array([
            [
                [1, 0.5, 0.3],
                [0.01, 0.5, 0.3],
                [1, 0.5, 0.3],
            ],
            [
                [0, 0.5, 0.31],
                [0, 0.51, 0.31],
                [0, 0.5, 0.29],
            ],
        ])
        self.assertEqual(expected.tolist(), result.tolist())

    def test_edge_intensity(self):
        img = array([
            [
                [1.01],
                [1.01],
                [1.01],
                [1.01],
                [1.01],
            ],
            [
                [0.99],
                [0.96],
                [0.02],
                [0.96],
                [0.99],
            ],
            [
                [0.96],
                [0.05],
                [0.01],
                [0.06],
                [0.96],
            ],
            [
                [0.99],
                [0.97],
                [0.97],
                [0.97],
                [0.99],
            ],
            [
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
            ],
        ])
        result = image.crop_background(img, bg_intensity=1, sim_threshold=0.1)
        expected = array([
            [
                [0.96],
                [0.02],
                [0.96],
            ],
            [
                [0.05],
                [0.01],
                [0.06],
            ],
        ])
        self.assertEqual(expected.tolist(), result.tolist())


class TestImage_resize_grayscale(TestCase):

    def test_integers_treated_correctly(self):
        src = array([
            [
                [1],
                [1],
                [1],
            ],
            [
                [0],
                [0],
                [0],
            ]
        ])
        result = image.resize_grayscale(src, (2, 2))
        expect = array([
            [
                [1],
                [1],
            ],
            [
                [0],
                [0],
            ]
        ])
        self.assertEqual(expect.tolist(), result.round(0).tolist())


class TestImage_pad(TestCase):
    def test_plain(self):
        src = array([
            [
                [0.5],
                [0.5],
            ],
            [
                [0.3],
                [0.4],
            ],
        ])
        result = image.pad(src, 2, padding_pixel=0.99)
        expected = array([
            [
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
            ],
            [
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
            ],
            [
                [0.99],
                [0.99],
                [0.5],
                [0.5],
                [0.99],
                [0.99],
            ],
            [
                [0.99],
                [0.99],
                [0.3],
                [0.4],
                [0.99],
                [0.99],
            ],
            [
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
            ],
            [
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
                [0.99],
            ],
        ])
        self.assertEqual(expected.tolist(), result.tolist())


class TestImage_convert_colour(TestCase):
    def test_grayscale_transparency(self):
        with open('resources/image-transparent.png', 'rb') as src:
            img = from_binary(src.read())
            result = image.convert_colour(img, transparency_colour=255, colour=cv2.COLOR_BGRA2GRAY)
            with open('resources/image-grayscale.png', 'rb') as exp:
                expected = from_binary(exp.read())
                self.assertEqual(expected.tolist(), result.tolist())
