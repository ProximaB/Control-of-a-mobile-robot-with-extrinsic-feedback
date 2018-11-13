import cv2
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# import numpy as np


def GuassianBlur(kernel=(15, 15)):

    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    while True:
        frame = vs.read()
        if frame is None:
            break
        frame = imutils.resize(frame, width=600)
        # _, frame = cap.read()
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # hsv hue sat value
        # lower_green = np.array([30, 180, 30])
        # upper_green = np.array([188, 250, 195])

        # mask = cv2.inRange(hsv, lower_green, upper_green)
        # res = cv2.bitwise_and(frame, frame, mask=mask)

        # cv2.circle(res, (100, 63), 55, (30, 180, 30), -1)
        # cv2.circle(res, (155, 63), 55, (110, 237, 0), -1)
        # cv2.circle(res, (210, 63), 55, (195, 250, 188), -1)

        # cv2.namedWindow('frame', cv2.WINDOW_GUI_EXPANDED)
        # cv2.namedWindow('mask', cv2.WINDOW_GUI_EXPANDED)
        # cv2.namedWindow('result', cv2.WINDOW_GUI_EXPANDED)
        # cv2.namedWindow('smoothed', cv2.WINDOW_GUI_EXPANDED)
        # cv2.namedWindow('GaussianBlur', cv2.WINDOW_GUI_EXPANDED)
        # cv2.namedWindow('median', cv2.WINDOW_GUI_EXPANDED)
        # cv2.namedWindow('bilaterail', cv2.WINDOW_GUI_EXPANDED)

        # kernel = np.ones((15,15), np.float32)/255

        # smoothed = cv2.filter2D(res, -1, kernel)

        blur = cv2.GaussianBlur(frame, kernel, 0)

        # cv2.putText(blur, 'Kernel: ' + str(kernel) + ', Type: Guassian Blur',
        #             org=(2, +30),
        #             fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=1,
        #             color=(255, 255, 255),
        #             thickness=2)
        # median = cz2.medianBlur(res, 15)

        # bilaterail = cv2.bilateralFilter(res, 15, 75, 75)

        # cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask)
        # cv2.imshow('result', res)
        # cv2.imshow('smoothed', smoothed)
        cv2.imshow('GaussianBlur', blur)
        # cv2.imshow('median', median)
        # cv2.imshow('bilaterail', bilaterail)

        k=cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    vs.release()
    print('waitKey')
    print("Test module works!")
