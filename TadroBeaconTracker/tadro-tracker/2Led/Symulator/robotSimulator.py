﻿import cv2 as cv
import numpy as np
import sys
import operator
import math
from math import cos, sin
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
from logger import *
from statusWindow import statusWindowText
from robot import Robot2Led
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/Symulator')
from RobotModel2Led import RobotModel2Led
# class robotSimulator:
#Przekształcić do klasy, która będzie przechowywała stan i na wywołanie nextframe(input values for model)
# zwróci kolejną klatkę,
W_HEIGHT = 640
W_WIDTH = 1280
D_MARGIN_HORIZONTAL = (150, 10) #(L,R)
D_MARGIN_VERTICAL = (10, 10)
FONT = cv.FONT_HERSHEY_SIMPLEX
    
D_WIDTH = W_WIDTH - D_MARGIN_HORIZONTAL[0] - D_MARGIN_HORIZONTAL[1]
D_HEIGHT = W_HEIGHT - D_MARGIN_VERTICAL[0] - D_MARGIN_VERTICAL[1]

LED_RADIUS = 8
LED_THICKNES = -1#8
ROBOT_THICKNESS = 3

AREA_POINTS = [(10,10), (-10,-10)] #punkty pola dodawane marginesy wys szer
AREA_THICKNESS = 4

def add(a, b):
    '''dodanie dwoch punktow, tuple '''
    return tuple(map(operator.add, a, b))
    
class robotSimulationEnv:
    def __init__(self, model : RobotModel2Led, tracker = None):
        self.model = model
        self.tracker = tracker

    def draw_robot_position(self, frame):
        #sw = statusWindowText(frame)
        #sw.drawData((50,50), 1.23, 10, 1.42, (255,0,0))
        robot =  self.model.robot
        led1_pos, led2_pos, time, robot_center, heading, diamater, axle_len = robot.unpack()
        #leds
        cv.circle(frame, led1_pos, LED_RADIUS, (0, 255, 0), LED_THICKNES)
        cv.circle(frame, led2_pos, LED_RADIUS, (0, 0, 255), LED_THICKNES)
        #robot circle
        rnd = tuple(map(round, robot_center))
        cv.circle(frame, rnd, round(diamater/2), (0, 0, 0), ROBOT_THICKNESS)
        #robot front half circle
        #radiu jest loiczny od roztawu kół nie od szerokosci robota.. któa jest wykorzystywana do rysowania
        radius=round(axle_len/2 - axle_len/2 * 0.2); axes = (radius,radius)
        angle=heading*180/np.pi
        startAngle=-30; endAngle=30#0-180def
        color=(255, 0, 0)
        cv.ellipse(frame, rnd, axes, angle, startAngle, endAngle, color, ROBOT_THICKNESS)
        #pole robocze robota
        shape_hw = frame.shape[1::-1]
        cv.rectangle(frame, AREA_POINTS[0], add(shape_hw, AREA_POINTS[1]), 0, AREA_THICKNESS)

    def simulation_keys_KLIO(self):
        win_frame = np.ones((W_HEIGHT, W_WIDTH, 3), dtype='uint8')
        display_frame = np.ones((D_HEIGHT, D_WIDTH, 3), dtype='uint8') *255 # white plane

        #Symulacja Robota
        #rysowanie_pozycji robota
        L = 0; R = 0
        while True:
            display_frame = np.ones((D_HEIGHT, D_WIDTH, 3),
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

            print(f'L:{L} R:{R}')
            model.simulate_robot_process(L, R, 1.0)
            robot.calculate_led_pos()

            self.draw_robot_position(display_frame)
            #wyświetlanie okna prezentującego symulacje i ważne parametry robota
            win_frame = np.ones((W_HEIGHT, W_WIDTH, 3), dtype='uint8') #czyszczenie win_frame
            win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame
            # wypisywanie statusu
            sw = statusWindowText(win_frame)
            sw.drawData(robot.robot_center, robot.heading, 0, 0)
            #wyswietlenie na oknie
            cv.imshow('result', win_frame)
        # nakładanie display_frame na win_frame
        win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame

        # wypisywanie statusu
        sw = statusWindowText(win_frame)    
        sw.drawData((100,200), 1.23, 10, 1.42)

        cv.imshow('result', win_frame)
        cv.waitKey(0)


    def simulate_return_image(self, vel_0, vel_1, time_diff=1):
        win_frame = np.ones((W_HEIGHT, W_WIDTH, 3), dtype='uint8')
        display_frame = np.ones((D_HEIGHT, D_WIDTH, 3), dtype='uint8') *255 # white plane

        #Symulacja Robota
        #rysowanie_pozycji robota
        print(f'L:{vel_0} R:{vel_1}')
        model.simulate_robot_process(vel_0, vel_1, time_diff)
        robot.calculate_led_pos()

        self.draw_robot_position(display_frame)
        
        #wyświetlanie okna prezentującego symulacje i ważne parametry robota
        win_frame = np.ones((W_HEIGHT, W_WIDTH, 3), dtype='uint8') #czyszczenie win_frame
        win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame
        
        # wypisywanie statusu
        sw = statusWindowText(win_frame)
        sw.drawData(robot.robot_center, robot.heading, 0, 0)
        #wyswietlenie na oknie
        cv.imshow('result', win_frame)
        # nakładanie display_frame na win_frame
        win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame
        #wyswitlanie podglądu symulacji w osobnym oknie
        cv.imshow('result', win_frame)

        return display_frame

if __name__ == "__main__":
    robot = Robot2Led(20, (500, 500), (500, 480), (500, 520), 0, 75, 50, 5)
    model = RobotModel2Led(robot, 5)
    sim = robotSimulationEnv(model, None)
    pic1 = sim.simulate_return_image(0,0,1)
    pic2 = sim.simulate_return_image(2,-2,2)
    cv.imshow('1', pic1)
    cv.imshow('2', pic2)
    cv.waitKey(0)
    #sim.simulation_keys_KLIO()


    #simulation_test_robot()
    #simulation_keys_KLIO()
    #simulation_keys_JKL()
