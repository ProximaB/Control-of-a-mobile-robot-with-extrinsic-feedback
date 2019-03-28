import numpy as np
import cv2 as cv


class ImgButton:
    def __init__(self, x_pos, y_pos, text = "TEST", width=20, height=10, colorOn= (0, 255, 0), colorOff= (0, 0, 255)):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height  = height
        self.colorOn = colorOn
        self.colorOff = colorOff
        self.text = text
        self.Toggle = True

    def draw_button(self, image):

        h, w = self.height, self.width
        button = np.ones((h, w, 3), dtype="uint8")

        m = 5
        if image.shape[0] < 10 or image.shape[1] < 10:
            return
        image[-h-self.x_pos:-self.x_pos, self.y_pos:w+self.y_pos] = button   # BL
        
    def contains(self, x, y):
        result = self.x_pos+self.width < x < self.y_pos+self.height
        return result

    def click(self):
        if self.Toggle:
            self.Toggle = False
        else:
            self.Toggle = True