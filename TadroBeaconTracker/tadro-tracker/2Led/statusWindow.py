import cv2 as cv
import numpy as np
class statusWindow:
    def __init__(self, win_name):
        self.win_name = win_name
        self.image = np.zeros((145,170), dtype='uint8')
    
    def drawData(self, x, y, orientation, error):
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(self.image, f'X:  {x}', (1, 33), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'Y:  {y}', (1, 66), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'Th: {orientation}', (1,99), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'E:  {error}', (1,132), font, 1, (255,255,255), 2, cv.LINE_AA)
        #cv.namedWindow(self.win_name, cv.WINDOW_FREERATIO)
        cv.imshow(self.win_name, self.image)


