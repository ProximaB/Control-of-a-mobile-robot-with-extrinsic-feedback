import cv2 as cv
import numpy as np
import sys
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
from logger import *
from statusWindow import statusWindowText

W_HEIGHT = 1280
W_WIDTH = 640
D_PADDING_H = (30, 10) #(L,R)
D_PADDING_V = (20, 10)
FONT = cv.FONT_HERSHEY_SIMPLEX
    
D_WIDTH = W_WIDTH - D_PADDING_H[0] - D_PADDING_H[1]
D_HEIGHT = W_HEIGHT - D_PADDING_V[0] - D_PADDING_V[1]

win_frame = np.ones((W_WIDTH, W_HEIGHT, 3), dtype='uint8')
display_frame = np.ones((D_WIDTH, D_HEIGHT, 3), dtype='uint8') *255 # white plane

win_frame[D_PADDING_H[0] : - D_PADDING_H[1], D_PADDING_V[0] : - D_PADDING_V[1]] = display_frame


sw = statusWindowText(win_frame)
sw.drawData((100,200), 1.23, 10, 1.42)

cv.imshow('result', win_frame)
cv.waitKey(0)