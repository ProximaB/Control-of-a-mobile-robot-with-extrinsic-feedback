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
    def __init__(self, DATA):
        DATA.created_images = False
        self.time = time.clock()

    def find_arruco(self, DATA, SETTINGS):
        image = DATA.processed_image
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        #gray = cv.bilateralFilter(gray, 4,4,4)
        aruco_dict = aruco.Dictionary_get(CFG.ARUCO_DICT)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if not corners:
            return None
        DATA.base_image = aruco.drawDetectedMarkers(DATA.base_image, corners)
        
        return corners
    
    def midpoint(self, p1, p2):
        return  ((p1[0]+p2[0])/2.0, (p1[1]+p2[1])/2.0)

    def detectAndTrack(self, SETTINGS, DATA, ROBOT):
        if DATA.base_image is None:
            raise Exception("No base_iamge provided. {->detectAndTrack2LedRobot}")
        #for prfm get rid of it
        DATA.processed_image = DATA.base_image.copy()

        robot_ctour = self.find_arruco(DATA, SETTINGS)
        if robot_ctour is None:
            cv.imshow('Tracing and Recognition.', DATA.base_image)
            return ROBOT
        robot_ctour 
        LT, RT, RB, LB = robot_ctour[0][0]

        robot_center_img = self.midpoint(LT, RB)
        
        hI, wI, _ = DATA.processed_image.shape
        imgMax = (hI, wI)

        hR, wR = CFG.AREA_HEIGHT_REAL, CFG.AREA_WIDTH_REAL
        realMax = (hR, wR)

        target = map_point_to_img(DATA.target, imgMax, realMax)
        DATA.robot_center = map_point_to_real(robot_center_img, imgMax, realMax)

        DATA.heading =  math.atan2(RB[0]-LT[0], RB[1]-LT[1]) + -np.pi
        DATA.heading = -1 * math.atan2(math.sin(DATA.heading), math.cos(DATA.heading))
        DATA.base_image = aruco.drawDetectedMarkers(DATA.base_image, robot_ctour)
        # updatee the displays:
        cv.circle(DATA.base_image, target, 3, (255,0,0), 2, -1)
        cv.imshow('Tracing and Recognition.', DATA.base_image)
        
        if (DATA.robot_center and DATA.heading) != ('' or None):
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