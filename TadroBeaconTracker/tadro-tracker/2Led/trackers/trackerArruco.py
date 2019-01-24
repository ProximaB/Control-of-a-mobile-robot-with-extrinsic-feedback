import time
import numpy as np
import cv2 as cv
import sys
import math
import pickle
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG
from utils import *

class TrackArruco:
    def __init__(self, DATA):
        DATA.created_images = False
        self.time = time.clock()

    def find_arruco(self, DATA, SETTINGS):
        pass
    
    def detectAndTrack(self, SETTINGS, DATA, ROBOT):
        """ this function organizes all of the processing
            done for each image from a camera type 2Led robot """
        # somewhere self.find_arruco()
        if DATA.base_image is None:
            raise Exception("No base_iamge provided. {->detectAndTrack2LedRobot}")
        DATA.processed_image = DATA.base_image
        # updatee the displays:
        cv.circle(DATA.base_image, DATA.target, 3, (255,0,0), 2, -1)
        cv.imshow('Tracing and Recognition.', DATA.base_image)
        if (DATA.robot_center and DATA.led2_pos) != ('' or None):
            return ROBOT.update(time.clock() - self.time, DATA.robot_center, DATA.heading)
        else: return ROBOT

    # Callback zachowanie dla przycisków i z pętlą dla przyciskow ustawiajacy wyswietlany thresh
    def check_key_press(self, key_press, DATA, SETTINGS):

        SETTINGS.last_key_pressed = key_press

        # if it was ESC, make it 'q'
        if key_press == 27:
            key_press = ord('q')

        # if a 'q' or ESC was pressed, we quit
        if key_press == ord('q'): 
            print("Quitting")
            return