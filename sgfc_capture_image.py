#!/usr/bin/env python2

import cv2
import time

import sgfc_vision

from sgfc_communication.protobufs import sgfc_pb2 as fc_proto


camera_device = sgfc_vision.get_device(1)

for index in range(100):
    compressed_image = sgfc_vision.get_compressed_image(camera_device)
    print(index, len(compressed_image))

    cv2.imwrite('img.jpg',
                cv2.imdecode(compressed_image, cv2.CV_LOAD_IMAGE_COLOR),
                [cv2.IMWRITE_JPEG_QUALITY, sgfc_vision.DEFAULT_JPEG_QUALITY])
