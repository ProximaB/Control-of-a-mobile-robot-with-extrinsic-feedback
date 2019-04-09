import cv2 as cv
import numpy as np
class statusWindow:
    def __init__(self, win_name):
        self.win_name = win_name
        self.image = np.zeros((227,367), dtype='uint8')
        cv.namedWindow(self.win_name)
        cv.moveWindow(self.win_name, 0, 0)
    
    def drawData(self, position, heading, error, heading_error, doWarping, detected = True):
        x, y = position
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(self.image, f'X:   {round(x, ndigits = 3)} mm', (1, 33), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'Y:   {round(y, ndigits = 3)} mm', (1, 66), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, 'Th:  {0}'.format(round(heading*180.0/np.pi, ndigits=3)), (1,99), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'E:   {round(error, ndigits = 3)}mm', (1,132), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'ThE: {round(heading_error*180.0/np.pi, ndigits=3)}', (1,165), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'Do warp: {doWarping}', (1,195), font, 1, (255,255,255), 2, cv.LINE_AA)
        cv.putText(self.image, f'Robot Detected: {detected}', (1,225), font, 1, (255,255,255), 2, cv.LINE_AA)

        #cv.namedWindow(self.win_name, cv.WINDOW_FREERATIO)
        cv.imshow(self.win_name, self.image)
       

class statusWindowText:
    def __init__(self, image):
        self.image = image
    
    def drawData(self, position, heading, error, heading_error, color=(255,255,255)):
        x, y = position
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(self.image, f'X:   {round(x, ndigits= 3)}', (1, 33), font, 1, color, 2, cv.LINE_AA)
        cv.putText(self.image, f'Y:   {round(y, ndigits = 3)}', (1, 66), font, 1, color, 2, cv.LINE_AA)
        cv.putText(self.image, 'Th:  {0}'.format(round(heading*180.0/np.pi, ndigits = 3)), (1,99), font, 1, color, 2, cv.LINE_AA)
        #cv.putText(self.image, f'E:   {error}', (1,132), font, 1, color, 2, cv.LINE_AA)
        #cv.putText(self.image, f'ThE: {round(heading_error*180.0/np.pi)}', (1,165), font, 1, color, 2, cv.LINE_AA)


