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
# import Robot clases
from robot import Robot, Robot2Led, RobotAruco

import cv2.aruco as aruco

class TrackArruco:
    def __init__(self, ):
        DATA.created_images = False
        self.time = time.clock()

    def find_arruco(self, DATA, SETTINGS):
        image = DATA.processed_image
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(CFG.ARUCO_DICT)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
        DATA.base_image = aruco.drawDetectedMarkers(DATA.base_image, corners)
        return 
    
    def midpoint(self, p1, p2):
        return  ((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

    def detectAndTrack(self, SETTINGS, DATA, ROBOT):
        if DATA.base_image is None:
            raise Exception("No base_iamge provided. {->detectAndTrack2LedRobot}")
        image = DATA.base_image
        RB, LB, LT, RT = DATA.robot_cntr
        robot_center_img = self.midpoint(RB, LT)
        
        hI, wI, _ = DATA.processed_image.shape
        imgMax = (hI, wI)

        hR, wR = CFG.AREA_HEIGHT_REAL, CFG.AREA_WIDTH_REAL
        realMax = (hR, wR)

        ROBOT.robot_center = map_point_to_img(robot_center_img, imgMax, realMax)

        ROBOT.heading =  math.atan2(RB[0]-LT[0], RB[1]-LT[1]) + -np.pi
        ROBOT.heading = -1 * math.atan2(math.sin(ROBOT.heading), math.cos(ROBOT.heading))

        DATA.base_image = aruco.drawDetectedMarkers(DATA.base_image, DATA.robot_cntr)
        # updatee the displays:
        cv.circle(DATA.base_image, )
        cv.circle(DATA.base_image, DATA.target, 3, (255,0,0), 2, -1)
        cv.imshow('Tracing and Recognition.', self.DATA.base_image)
        
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