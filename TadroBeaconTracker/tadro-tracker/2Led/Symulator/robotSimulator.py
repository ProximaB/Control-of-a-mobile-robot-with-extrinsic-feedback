import cv2 as cv
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
def draw_robot_position(robot : Robot2Led, frame):
    #sw = statusWindowText(frame)
    #sw.drawData((50,50), 1.23, 10, 1.42, (255,0,0))
    
    led1_pos, led2_pos, time, robot_center, heading, diamater = robot.unpack()
    #leds
    cv.circle(frame, led1_pos, LED_RADIUS, (0, 255, 0), LED_THICKNES)
    cv.circle(frame, led2_pos, LED_RADIUS, (0, 0, 255), LED_THICKNES)
    #robot circle
    rnd = tuple(map(math.ceil, robot_center))
    cv.circle(frame, rnd, round(diamater/2), (0, 0, 0), ROBOT_THICKNESS)
    #robot front half circle
    radius=round(diamater/2 - diamater/2 * 0.2); axes = (radius,radius)
    angle=heading*180/np.pi
    startAngle=60; endAngle=120#0-180def
    color=(255, 0, 0)
    cv.ellipse(frame, rnd, axes, angle, startAngle, endAngle, color, ROBOT_THICKNESS)
    #pole robocze robota
    shape_hw = frame.shape[1::-1]
    cv.rectangle(frame, AREA_POINTS[0], add(shape_hw, AREA_POINTS[1]), 0, AREA_THICKNESS)

def simulation_keys_JKL():
    win_frame = np.ones((W_HEIGHT, W_WIDTH, 3), dtype='uint8')
    display_frame = np.ones((D_HEIGHT, D_WIDTH, 3), dtype='uint8') *255 # white plane

    #Symulacja Robota
    # -> wrzucamy model z potrzebnymi parametrami, ktory zwraca pozycje w danym czasie
    robot = Robot2Led(20, (500, 500), (500, 480), (500, 520), 0, 75, 40)
    #rysowanie_pozycji robota
    draw_robot_position(robot, display_frame)

    model = RobotModel2Led(robot, 10)
    model.simulate_robot_process(0,0,1)

    cv.imshow('result', win_frame)

    '''for i in range(1, 90, 1):
        display_frame = np.ones((D_HEIGHT, D_WIDTH, 3), dtype='uint8') *255 # white plane
        print(f'i={i}')
        if i < 10:
            model.simulate_robot_process(19, 1, 1)
        elif i < 30:
            model.simulate_robot_process(1, 2, 1)
        elif i < 60:
            model.simulate_robot_process(-1, 1, 1)
        else:
            model.simulate_robot_process(1, 1, 1)
        '''
    while True:
        display_frame = np.ones((D_HEIGHT, D_WIDTH, 3),
                                dtype='uint8') * 255  # white plane
        key = cv.waitKey(10)

        if key == ord('j'):
            model.simulate_robot_process(3.9, 3.2, 1.0)
        elif key == ord('k'):
            model.simulate_robot_process(-0.9, -0.2, 1.0)
        elif key == ord('l'):
            model.simulate_robot_process(1, 1, 1.0)
        else:
            pass#model.simulate_robot_process(0, 0, 1.0)
        robot.calculate_led_pos()
        #phi = math.atan2(p1[0]-p2[0], p1[1]-p2[1])
        draw_robot_position(robot, display_frame)

        win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame
        # wypisywanie statusu
        sw = statusWindowText(win_frame)
        sw.drawData((100,200), 1.23, 10, 1.42)
        cv.imshow('result', win_frame)
        #cv.waitKey(300)
    # nakładanie display_frame na win_frame
    win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame

    # wypisywanie statusu
    sw = statusWindowText(win_frame)
    sw.drawData((100,200), 1.23, 10, 1.42)

    cv.imshow('result', win_frame)
    cv.waitKey(0)

def simulation_keys_KL():
    win_frame = np.ones((W_HEIGHT, W_WIDTH, 3), dtype='uint8')
    display_frame = np.ones((D_HEIGHT, D_WIDTH, 3), dtype='uint8') *255 # white plane

    #Symulacja Robota
    # -> wrzucamy model z potrzebnymi parametrami, ktory zwraca pozycje w danym czasie
    robot = Robot2Led(20, (500, 500), (500, 480), (500, 520), 0, 75, 40)
    #rysowanie_pozycji robota
    draw_robot_position(robot, display_frame)

    model = RobotModel2Led(robot, 10)
    model.simulate_robot_process(0,0,1)

    cv.imshow('result', win_frame)

    '''for i in range(1, 90, 1):
        display_frame = np.ones((D_HEIGHT, D_WIDTH, 3), dtype='uint8') *255 # white plane
        print(f'i={i}')
        if i < 10:
            model.simulate_robot_process(19, 1, 1)
        elif i < 30:
            model.simulate_robot_process(1, 2, 1)
        elif i < 60:
            model.simulate_robot_process(-1, 1, 1)
        else:
            model.simulate_robot_process(1, 1, 1)
        '''
    L = 0; R = 0
    while True:
        display_frame = np.ones((D_HEIGHT, D_WIDTH, 3),
                                dtype='uint8') * 255  # white plane
        key = cv.waitKey(10)

        if key == ord('k'):
            L += 0.2
        elif key == ord('l'):
            R += 0.2
        if key == ord('i'):
            L -= 0.2
        elif key == ord('o'):
            R -= 0.2
        print(f'L:{L} R:{R}')
        model.simulate_robot_process(L, R, 1.0)
        robot.calculate_led_pos()
        #phi = math.atan2(p1[0]-p2[0], p1[1]-p2[1])
        draw_robot_position(robot, display_frame)

        win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame
        # wypisywanie statusu
        sw = statusWindowText(win_frame)
        sw.drawData((100,200), 1.23, 10, 1.42)
        cv.imshow('result', win_frame)
        #cv.waitKey(300)
    # nakładanie display_frame na win_frame
    win_frame[D_MARGIN_VERTICAL[0] : - D_MARGIN_VERTICAL[1], D_MARGIN_HORIZONTAL[0] : - D_MARGIN_HORIZONTAL[1], ] = display_frame

    # wypisywanie statusu
    sw = statusWindowText(win_frame)
    sw.drawData((100,200), 1.23, 10, 1.42)

    cv.imshow('result', win_frame)
    cv.waitKey(0)

if __name__ == "__main__":
    simulation_keys_KL()
    #simulation_keys_JKL()