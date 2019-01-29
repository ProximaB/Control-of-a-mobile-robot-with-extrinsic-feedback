import cv2 as cv
import numpy as np
import sys
import operator
import math
from math import cos, sin
import cv2.aruco as aruco
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
from config import D as CFG
from logger import *
from statusWindow import statusWindowText
from robot import Robot2Led
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/Symulator')
from RobotModel2Wheels import RobotModel2Wheels

from scipy import ndimage
# class robotSimulator:
#Przekształcić do klasy, która będzie przechowywała stan i na wywołanie nextframe(input values for model)
# zwróci kolejną klatkę,

def add(a, b):
    '''dodanie dwoch punktow, tuple '''
    return tuple(map(operator.add, a, b))
    
class robotSimulationEnv2Led:
    def __init__(self, model : RobotModel2Wheels):
        self.model = model

        self.aruco_corners_img = [] 
        aruco_dict = aruco.Dictionary_get(CFG.ARUCO_DICT)
        for i, _id in enumerate(CFG.CORNER_IDS):
            aruco_img = aruco.drawMarker(aruco_dict, id = _id, sidePixels = CFG.SIDEPIXEL_ARUCO)
            aruco_img =cv.cvtColor(aruco_img, cv.COLOR_GRAY2BGR)
            aruco_img = ndimage.rotate(aruco_img, 180 - 90*i)

            self.aruco_corners_img.append(aruco_img)

    def draw_robot_position(self, frame):
        # draw arruco corner markers
        ar_arr = self.aruco_corners_img
        h, w, c = ar_arr[0].shape
        
        m = CFG.MARGIN_ARUCO
        frame[m:h+m, m:w+m] = ar_arr[0]   # UL
        frame[m:h+m, -w-m:-m] = ar_arr[1] # UR
        frame[-h-m:-m, -w-m:-m] = ar_arr[2]  # BR
        frame[-h-m:-m, m:w+m] = ar_arr[3]   # BL
        #frame[10:h:,-w-10:-10] = ar_arr[1]
        #frame[10:h,10:w] = ar_arr[2]
        #frame[10:h,10:w] = ar_arr[3]

        #sw = statusWindowText(frame)
        #sw.drawData((50,50), 1.23, 10, 1.42, (255,0,0))
        robot =  self.model.robot
        height, width, cnl = frame.shape

        true_height = height - 2*(m+h)
        true_width = width - 2*(m+w)
        area_frame = np.ones((true_height, true_width, 3), dtype='uint8') *255

        led1_pos, led2_pos, time, robot_center, heading, diamater, axle_len = robot.unpackImg(true_height, CFG.AREA_HEIGHT_REAL, true_width, CFG.AREA_WIDTH_REAL)
        #leds
        cv.circle(area_frame, led1_pos, CFG.LED_RADIUS, (0, 255, 0), CFG.LED_THICKNES)
        cv.circle(area_frame, led2_pos, CFG.LED_RADIUS, (0, 0, 255), CFG.LED_THICKNES)
        #robot circle
        rnd = tuple(map(round, robot_center))
        cv.circle(area_frame, rnd, round(diamater/2), (0, 0, 0), CFG.ROBOT_THICKNESS)
        #robot front half circle
        #radiu jest loiczny od roztawu kół nie od szerokosci robota.. któa jest wykorzystywana do rysowania
        radius=round(axle_len/2 - axle_len/2 * 0.2); axes = (radius,radius)
        angle=heading*180/np.pi
        startAngle=-30; endAngle=30#0-180def
        color=(255, 0, 0)
        cv.ellipse(area_frame, rnd, axes, angle, startAngle, endAngle, color, CFG.ROBOT_THICKNESS)
        #pole robocze robota
        mh = m+h
        mw = m+w
        frame[mw: -mw, mh: -mh] = area_frame
        # shape_hw = frame.shape[1::-1]
        #cv.rectangle(frame, CFG.AREA_POINTS[0], add(shape_hw, CFG.AREA_POINTS[1]), 0, CFG.AREA_THICKNESS)

    def simulation_keys_KLIO(self):
        win_frame = np.ones((CFG.W_HEIGHT, CFG.W_WIDTH, 3), dtype='uint8')
        display_frame = np.ones((CFG.D_HEIGHT, CFG.D_WIDTH, 3), dtype='uint8') *255 # white plane

        #Symulacja Robota
        #rysowanie_pozycji robota
        L = 0; R = 0
        while True:
            display_frame = np.ones((CFG.D_HEIGHT, CFG.D_WIDTH, 3),
                                    dtype='uint8') * 255  # white plane
            key = cv.waitKey(5)

            if key == ord('i'):
                L += 0.02
            elif key == ord('o'):
                R += 0.02
            if key == ord('k'):
                L -= 0.02
            elif key == ord('l'):
                R -= 0.02
            elif key == ord('q'):
                break;

            log_print(f'L:{L} R:{R}')
            model.simulate_robot_process(L, R, 1.0)
            robot.calculate_led_pos()

            self.draw_robot_position(display_frame)
            #wyświetlanie okna prezentującego symulacje i ważne parametry robota
            win_frame = np.ones((CFG.W_HEIGHT, CFG.W_WIDTH, 3), dtype='uint8') #czyszczenie win_frame
            win_frame[CFG.D_MARGIN_VERTICAL[0] : - CFG.D_MARGIN_VERTICAL[1], CFG.D_MARGIN_HORIZONTAL[0] : - CFG.D_MARGIN_HORIZONTAL[1], ] = display_frame
            # wypisywanie statusu
            sw = statusWindowText(win_frame)
            sw.drawData(robot.robot_center, robot.heading, 0, 0)
            #wyswietlenie na oknie
            cv.imshow('result', win_frame)
        # nakładanie display_frame na win_frame
        win_frame[CFG.D_MARGIN_VERTICAL[0] : - CFG.D_MARGIN_VERTICAL[1], CFG.D_MARGIN_HORIZONTAL[0] : - CFG.D_MARGIN_HORIZONTAL[1], ] = display_frame

        # wypisywanie statusu
        sw = statusWindowText(win_frame)    
        sw.drawData((100,200), 1.23, 10, 1.42)

        cv.imshow('result', win_frame)
        cv.waitKey(0)


    def simulate_return_image(self, vel_0, vel_1, time_diff=1):
        model = self.model
        robot = model.robot
        
        win_frame = np.ones((CFG.W_HEIGHT, CFG.W_WIDTH, 3), dtype='uint8')
        display_frame = np.ones((CFG.D_HEIGHT, CFG.D_WIDTH, 3), dtype='uint8') *255 # white plane

        #Symulacja Robota
        #rysowanie_pozycji robota
        log_print(f'L:{vel_0} R:{vel_1}')
        model.simulate_robot_process(vel_0, vel_1, time_diff)
        robot.calculate_led_pos()

        self.draw_robot_position(display_frame)
        
        #wyświetlanie okna prezentującego symulacje i ważne parametry robota
        win_frame = np.ones((CFG.W_HEIGHT, CFG.W_WIDTH, 3), dtype='uint8') #czyszczenie win_frame
        # wypisywanie statusu
        sw = statusWindowText(win_frame)
        sw.drawData(robot.robot_center, robot.heading, 0, 0)
        # nakładanie display_frame na win_frame
        win_frame[CFG.D_MARGIN_VERTICAL[0] : - CFG.D_MARGIN_VERTICAL[1], CFG.D_MARGIN_HORIZONTAL[0] : - CFG.D_MARGIN_HORIZONTAL[1], ] = display_frame
        #wyswitlanie podglądu symulacji w osobnym oknie
        cv.imshow('Simulator Window', win_frame)

        return display_frame

if __name__ == "__main__":
    aruco_dict = aruco.Dictionary_get(CFG.ARUCO_DICT)
    arruco_img = aruco.drawMarker(aruco_dict, id = 1, sidePixels = 30)

    robot = Robot2Led(0, CFG.ROB_CNTR, None, None, CFG.HEADING, CFG.DIAMETER, CFG.AXLE_LEN, CFG.WHEEL_RADIUS)
    robot.calculate_led_pos()
    model = RobotModel2Wheels(robot, 5)
    sim = robotSimulationEnv2Led(model)
    class cap:
        def read(self, x,y,z): return sim.simulate_return_image(x,y,z)
    
    capture = cap()
    pic1 = sim.simulate_return_image(0,0,1)
    pic2 = sim.simulate_return_image(2,-2,2)
    pic3 = capture.read(2,4,4)
    cv.imshow('1', pic1)
    cv.imshow('2', pic2)
    cv.imshow('3', pic3)
    cv.waitKey(0)
    #sim.simulation_keys_KLIO()


    #simulation_test_robot()
    #simulation_keys_KLIO()
    #simulation_keys_JKL()
