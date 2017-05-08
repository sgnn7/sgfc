#!/usr/bin/env python2

import cv2
import time

import sgfc_vision

from sgfc_communication.protobufs import sgfc_pb2 as fc_proto


cv2.startWindowThread()
cv2.namedWindow('image', cv2.WINDOW_NORMAL | cv2.WINDOW_AUTOSIZE)

compressed_image = sgfc_vision.get_compressed_image()


try:
    cv2.imshow('image', cv2.imdecode(compressed_image, 1))
    time.sleep(20)
finally:
    cv2.imwrite('img.jpg', compressed_image)
    cv2.destroyAllWindows()
