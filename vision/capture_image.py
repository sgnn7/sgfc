#!/usr/bin/env python

import cv2
import time

cap_left = cv2.VideoCapture(1)
cap_right = cv2.VideoCapture(2)

cv2.startWindowThread()
cv2.namedWindow('image', cv2.WINDOW_NORMAL | cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('image2', cv2.WINDOW_NORMAL | cv2.WINDOW_AUTOSIZE)

try:
    for index in range(100):
        print("Capturing %d" % index)
        ret, frame_left = cap_left.read()
        ret, frame_right = cap_right.read()
        # cv2.imwrite('image_%d.png' % index, frame)
        cv2.imshow('image', frame_left)
        cv2.imshow('image2', frame_right)
        # if cv2.waitKey(30) & 0xFF == ord('q'):
        #     break
finally:
    if cap_left:
        cap_left.release()
    if cap_right:
        cap_right.release()

    cv2.destroyAllWindows()
